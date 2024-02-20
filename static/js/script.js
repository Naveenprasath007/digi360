// file validation
var fileTypeDropdown = document.getElementById('typeInput');
var fileInput = document.getElementById('fileInput');

fileTypeDropdown.addEventListener('change', function() {
    var fileType = fileTypeDropdown.value;
    switch (fileType) {
        case 'VIDEO':
            fileInput.accept = 'video/*';
            break;
        case 'IMAGE':
            fileInput.accept = 'image/*';
            break;
        case 'GIF':
            fileInput.accept = '.gif/*';
            break;
        case 'PDF':
            fileInput.accept = '.pdf';
            break;
        default:
            fileInput.accept = '';
            break;
    }
});

// upload s3
var uploadQueue = [];
var isUploading = false;
var uploadLocations = []; // Array to store upload locations
var filesArray = []; // Array to store files for upload

var dropArea = document.getElementById('dropArea');
var fileList = document.getElementById('fileList');

dropArea.addEventListener('click', function() {
  document.getElementById('fileInput').click();
});

dropArea.addEventListener('dragover', function(e) {
  e.preventDefault();
  dropArea.classList.add('active');
});

dropArea.addEventListener('dragleave', function(e) {
  dropArea.classList.remove('active');
});

dropArea.addEventListener('drop', function(e) {
  e.preventDefault();
  dropArea.classList.remove('active');
  var files = e.dataTransfer.files;
  handleFiles(files);
});

document.getElementById('fileInput').addEventListener('change', function(e) {
  var files = e.target.files;
  handleFiles(files);
});

function handleFiles(files) {
    for (var i = 0; i < files.length; i++) {
      (function(file) {
        filesArray.push(file);
        var li = document.createElement('li');
        li.className = 'file-item';
  
        var fileNameSpan = document.createElement('span');
        fileNameSpan.className = 'file-name';
        fileNameSpan.textContent = file.name + ' (' + formatBytes(file.size) + ')';
        li.appendChild(fileNameSpan);
  
        var removeButton = document.createElement('button');
        removeButton.className = 'remove-button';
        removeButton.textContent = 'X';
        removeButton.addEventListener('click', function() {
          var index = filesArray.indexOf(file);
          if (index > -1) {
            filesArray.splice(index, 1);
            fileList.removeChild(li);
          }
        });
        li.appendChild(removeButton);
  
        fileList.appendChild(li);
      })(files[i]);
    }
  }
  

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  var k = 1024,
      dm = decimals < 0 ? 0 : decimals,
      sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
      i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function startUpload() {
    var creativeName = document.getElementById('creativeNameInput').value;
    // var files = document.getElementById('file-input').files;
    var creator = document.getElementById('creatorInput').value;
    var lob = document.getElementById('lobInput').value;
    var type = document.getElementById('typeInput').value;
    var platform = document.getElementById('platformInput').value;
    
    var creativeNameValidationMessage = '';
    var fileValidationMessage = '';
    var creatorValidationMessage = '';
    var lobValidationMessage = '';
    var typeValidationMessage ='';
    var platformValidationMessage ='';

    if (!creativeName) {
        creativeNameValidationMessage = 'Required!';
    }
    if (!creator) {
        creatorValidationMessage = 'Required!';
    }
    if (!lob) {
        lobValidationMessage = 'Required!';
    }
    if (!type) {
        typeValidationMessage = 'Required!';
    }
    if (!platform) {
        platformValidationMessage = 'Required!';
    }
    if (!filesArray.length > 0) {
        fileValidationMessage = 'At least one file must be selected.';
    }
    

    document.getElementById('creativeNameValidationMessage').innerHTML = creativeNameValidationMessage;
    document.getElementById('fileValidationMessage').innerHTML = fileValidationMessage;
    document.getElementById('creatorValidationMessage').innerHTML = creatorValidationMessage;
    document.getElementById('lobValidationMessage').innerHTML = lobValidationMessage;
    document.getElementById('typeValidationMessage').innerHTML = typeValidationMessage;
    document.getElementById('platformValidationMessage').innerHTML = platformValidationMessage;


    if (!creativeNameValidationMessage && !fileValidationMessage && !creatorValidationMessage && !lobValidationMessage && !typeValidationMessage && !platformValidationMessage) {
        const id = uuidv4();
        uploadQueue.push({ files: filesArray,id:id ,creativeName: creativeName,creator: creator,lob: lob,type: type,platform: platform });
        if (!isUploading) {
            processQueue();
        }
        document.getElementById('uploadButton').disabled = true; // Disable the upload button

    }
}

document.getElementById('uploadButton').addEventListener('click', startUpload);


function processQueue() {
    if (uploadQueue.length > 0) {
        isUploading = true;
        var item = uploadQueue.shift();
        uploadItem(item, function() {
            processQueue();
        });
    } else {
        isUploading = false;
        document.getElementById('uploadButton').disabled = false; // Re-enable the upload button
        console.log('All upload locations:', uploadLocations); // Log the list of upload locations
        clearForm(); // Clear the form once all uploads are complete
    }
}

function clearForm() {
    fileList.innerHTML = ''; // Clear file list
    filesArray = []; // Clear files array
    document.getElementById('creativeNameInput').value = ''
    document.getElementById('creatorInput').value = ''
    document.getElementById('lobInput').value = ''
    document.getElementById('typeInput').value = ''
    document.getElementById('platformInput').value = ''
    document.getElementById('option1').value = ''
    document.getElementById('option2').value = ''
    document.getElementById('option3').value = ''
    document.getElementById('option4').value = ''
    document.getElementById('option5').value = ''


    var progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = '0%';
    }

    // Clear the progress container
    var progressContainer = document.getElementById('progressContainer');
    if (progressContainer) {
        progressContainer.innerHTML = '';
    }
    $("#exampleModal").modal('toggle')
}
function uploadItem(item, callback) {
    var totalSize = item.files.reduce((acc, file) => acc + file.size, 0);
    var uploadedSize = 0;
    var fileProgress = {};
    var currentUploadLocations = []; // Array to store current set upload locations

    var progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    var progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressContainer.appendChild(progressBar);
    document.getElementById('progressContainer').appendChild(progressContainer);

    function updateProgress() {
        var progress = Math.round((uploadedSize / totalSize) * 100);
        progressBar.style.width = progress + '%';
    }

    function uploadNextFile() {
        if (item.files.length > 0) {
            var file = item.files.shift();
            var params = {
                Key: file.name,
                Body: file,
                ACL: 'public-read'
            };

            var options = {
                partSize: 10 * 1024 * 1024, // 10 MB
                queueSize: 1
            };

            var upload = s3.upload(params, options);

            upload.on('httpUploadProgress', function(event) {
                if (!fileProgress[file.name]) {
                    fileProgress[file.name] = 0;
                }
                uploadedSize += event.loaded - fileProgress[file.name];
                fileProgress[file.name] = event.loaded;
                updateProgress();
            });

            upload.send(function(err, data) {
                if (err) {
                    console.log('Error', err);
                } else {
                    console.log('Upload Success', data.Location);
                    currentUploadLocations.push({ fileName: file.name, fileLocation: data.Location }); // Add the file name and location to the current set
                }
                uploadNextFile();
            });
        } else {
            uploadLocations.push(currentUploadLocations); // Add the current set locations to the main list
            console.log(currentUploadLocations)
            saveUploadInfo(item, currentUploadLocations); // Save the entire set of file info at once
            console.log(item.creator)
            console.log(item.platform)
            callback();
        }
    }

    uploadNextFile();
}



function saveUploadInfo(item, fileLocations) {
  var data = {
      id:item.id,
      creativeName: item.creativeName,
      creator: item.creator,
      lob: item.lob,
      type: item.type,
      platform: item.platform,
      files: fileLocations,
      csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value
  };

  $.ajax({
      url: 'save-upload-info/',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', data.csrfmiddlewaretoken);
      },
      success: function(response) {
          console.log('Upload info saved:', response);
      },
      error: function(error) {
          console.log('Error saving upload info:', error);
      }
  })                   .done(function (data) {
    $("#example-form").trigger("reset");
    $.get('/cm/getajax/', function (response) {

    })
        .done(function (datas) {
            $("#dataTable > tbody").prepend("<tr id='table-" + datas.id + "'>\n\
            <td></td><td><input type='checkbox'></td><td class='ellipsis'><span>" + datas.name + "</span></td><td>" + datas.creator + "</td><td>" + datas.creative_type + "</td>\n\
        <td class='ellipsis'><span>" + datas.platform + "</span></td><td class='ellipsis'><span><a style='text-decoration:none' href='/cm/fileview/"+datas.id+"'>View Files</a></span></td>\n\
        <td>" + datas.created_at + "</td><td><a class='btn btn-sm btn-warning'><span class='fa fa-edit'></span>Edit</a>\n\
        <a class='btn btn-sm btn-danger delete' data-id='" + datas.id + "'><span class='fa fa-trash'></span> Delete</a> </td></tr>");
        numberRows();
        })
        .fail(function () {
            $("#fails").show();
        })

});

}







//random id generator
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    .replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0, 
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}



// multiselect
var expanded = false;

function showCheckboxes() {
  var checkboxes = document.getElementById("checkboxes");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}

function updateInputField() {
  var selectedOptions = [];
  var checkboxes = document.getElementById("checkboxes").querySelectorAll("input[type=checkbox]:checked");
  for (var i = 0; i < checkboxes.length; i++) {
    selectedOptions.push(checkboxes[i].value);
  }
  document.getElementById("platformInput").value = selectedOptions.join(", ");
}

function filterCheckboxes() {
  var input = document.getElementById("platformInput");
  var filter = input.value.toLowerCase();
  var checkboxes = document.getElementById("checkboxes");
  var labels = checkboxes.getElementsByTagName("label");

  for (var i = 0; i < labels.length; i++) {
    var label = labels[i];
    var text = label.textContent || label.innerText;
    if (text.toLowerCase().indexOf(filter) > -1) {
      label.style.display = "";
    } else {
      label.style.display = "none";
    }
  }
}

function selectAllCheckboxes() {
  var checkboxes = document.getElementById("checkboxes").querySelectorAll("input[type=checkbox]");
  var allChecked = true;
  for (var i = 0; i < checkboxes.length; i++) {
    if (!checkboxes[i].checked) {
      allChecked = false;
      break;
    }
  }
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = !allChecked;
  }
  updateInputField();
}


// FOR AUTOFILL SERIALNO
function numberRows() {
  var table = document.getElementById("dataTable");
  var rows = table.getElementsByTagName("tr");
  for (var i = 1; i < rows.length; i++) {
      rows[i].cells[0].innerHTML = i;
  }
}

window.onload = numberRows;

// reload before notify
window.addEventListener('beforeunload', function (e) {
  if (isUploading) {
      var message = 'Upload is in progress. Are you sure you want to leave?';
      e.returnValue = message;
      return message;
  }
});


// checkbox validation
document.getElementById("myForm").onsubmit = function() {
  var checkboxes = document.getElementsByName("checkbox");
  var isChecked = false;

  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      isChecked = true;
      break;
    }
  }

  if (!isChecked) {
    document.getElementById("alertMessage").style.display = "block";
    return false; // Prevent form submission
  }

  document.getElementById("alertMessage").style.display = "none";
  return true; // Allow form submission
};
