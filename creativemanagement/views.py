from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import threading
from django.core.files.storage import FileSystemStorage
from .models import Creative,UploadInfo
import os
import boto3
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# from aiohttp import web
# import asyncio
import datetime




from django.utils import timezone

# views.py
from django.http import HttpResponse
from django.shortcuts import render
import threading
import os
import shutil
import json
# views.py
from django.conf import settings
# from .tasks import upload_to_s3_and_save_chunk,upload_to_s3_and_save,process_uploaded_file
from django.core.serializers.json import DjangoJSONEncoder
import base64
aws_access_key_id=os.getenv('aws_access_key_id'),
aws_secret_access_key=os.getenv('aws_secret_access_key')
Bucketname=os.getenv('Bucketname')



def save_upload_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        creative = Creative(
            id=data['id'],
            name=data['creativeName'],
            creator=data['creator'],
            lob=data['lob'],
            creative_type=data['type'],
            platform=data['platform'],
            file_object_name=','.join([file['fileLocation'] for file in data['files']]),
            created_at=datetime.datetime.now(tz=timezone.utc),
            updated_at=datetime.datetime.now(tz=timezone.utc),

        )
        creative.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def fileview(request,id):
    if request.method == 'POST':
           return HttpResponse("Success!") 
    else:
        filtered_column_values = Creative.objects.filter(id=id).values_list('file_object_name', flat=True)
        url=filtered_column_values[0]
        url_list = url
        url_list = url_list.split(",")
        print(url_list)
        creative_type = Creative.objects.filter(id=id).values_list('creative_type', flat=True)
        type=creative_type[0]
        context = {
        'url_list': url_list,'type':type}
        # return HttpResponse("Success!") 
        return render(request, 'creativemanagement/fileView.html',context)

def getajax(request):
    if request.method == 'GET':
        if Creative(request):
            data = Creative.objects.order_by('-created_at').first()
            created = data.created_at.strftime('%m-%d-%Y %H:%M:%S')
            datas = {"id":data.id,"name": data.name, "creator": data.creator, "creative_type":data.creative_type,"file_object_name":data.file_object_name,
                     "platform": data.platform, "created_at": created}

            return JsonResponse(datas)
    else:
        return JsonResponse({'data': 'failure'})
    

def save_upload_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        creative = Creative(
            id=data['id'],
            name=data['creativeName'],
            creator=data['creator'],
            lob=data['lob'],
            creative_type=data['type'],
            platform=data['platform'],
            status="PENDING",
            file_object_name=','.join([file['fileLocation'] for file in data['files']]),
            created_at=datetime.datetime.now(tz=timezone.utc),
            updated_at=datetime.datetime.now(tz=timezone.utc),

        )
        creative.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def index(request):
    if request.method == 'POST':
            checkedbox=request.POST.getlist('checkbox')

            id_list = checkedbox  # List of IDs to update
            value = "WAIT FOR APPROVAL"

            for id in id_list:
                try:
                    obj = Creative.objects.get(id=id)
                    obj.status = value
                    # Update other attributes as needed
                    obj.save()
                except Creative.DoesNotExist:
                    # Handle the case when the object does not exist, e.g., log a message or create a new object
                    pass
            
            # creative_list = Creative.objects.order_by('-created_at')
            creative_list = Creative.objects.filter(status="PENDING").order_by('-created_at')
            context = {'creative_list': creative_list}
            return render(request, 'creativemanagement/index.html',context)

    # creative_list = Creative.objects.order_by('-created_at')
    creative_list = Creative.objects.filter(status="PENDING").order_by('-created_at')
    context = {'creative_list': creative_list}
    return render(request, 'creativemanagement/index.html',context)


# def save_upload_info(request):
#     if request.method == 'POST':
#         id=request.POST.get('id')
#         creativeName=request.POST.get('creativeName')
#         creator=request.POST.get('creator')
#         lob=request.POST.get('lob')
#         creativeType=request.POST.get('format')
#         platform=request.POST.get('platform')
#         obj = request.POST.getlist('files')
#         print(platform)

#         creative = Creative(id=id,name=creativeName,
#         creator=creator,lob=lob,creative_type=creativeType,
#         platform=platform,file_object_name=obj,status="Uploading")        
#         creative.save()
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'})





def uploadmulti(uploaded_file,filename):
    time.sleep(10)
    print('hi')
    # file_data=uploaded_file.read()
    # file_path = os.path.join(settings.MEDIA_ROOT, filename)
    # with open(file_path, 'wb') as f:
    #     f.write(file_data)







def serialize_video_file(uploaded_file,temp_file):
    # Extract relevant information
    byte=base64.b64encode(uploaded_file)
    file_info = {
        'name': temp_file.name,
        'size': temp_file.size,
        'content_base64': byte.decode('utf-8'),
        'content_type': temp_file.content_type,

    }

    # Serialize the information to JSON
    json_data = json.dumps(file_info, cls=DjangoJSONEncoder)
    uploadfil.delay(data=json_data)
    return json_data

# Usage


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file_content = request.FILES['file']
        # uploaded_file = request.FILES['file'].read()
        uploaded_name= request.FILES['file'].name
        # serialize_video_file.delay(uploaded_file,file_content)
        # serialize_video_file(uploaded_file,file_content)
        startTreading = threading.Thread(target=uploadmulti,args=(file_content,uploaded_name),daemon=True)
        startTreading.start()

        # process_uploaded_file.delay(uploaded_file, uploaded_name)
        


        # byte=base64.b64encode(uploaded_file)
        # file_info = {
        #     'name': file_content.name,
        #     'size': file_content.size,
        #     'content_base64': byte.decode('utf-8'),
        #     'content_type': file_content.content_type,

        # }

        # # Serialize the information to JSON
        # json_data = json.dumps(file_info, cls=DjangoJSONEncoder)
        # print(json_data)
        # Trigger the Celery task asynchronously


        # upload_to_s3_and_save.delay(uploaded_file,uploaded_file.name)

        # uploaded_file = request.FILES['file']
        # # Get the total number of chunks
        # total_chunks = int(request.POST.get('total_chunks', 1))
        # # Read and process each chunk
        # for i, chunk in enumerate(uploaded_file.chunks(), start=1):
        #     upload_to_s3_and_save_chunk.delay(chunk, i, total_chunks, uploaded_file.name, 'your-bucket-name', 'path/to/your/file')


        
        return JsonResponse({'message': 'File upload initiated successfully'}, status=200)
    else:
        return render(request, 'creativemanagement/upload_file.html')









def upload_to_s3(local_file_path, bucket_name, s3_key):
    start = time.time()
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key')
    )

    try:
        with open(local_file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, s3_key)
            print(f"File {local_file_path} uploaded to {bucket_name}/{s3_key}.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
    end = time.time()
    print("Single upload Time Taken",end - start)


# def upload(request):
#     if request.method == 'POST':
#         myfile = request.FILES['filename']
#         print(myfile)
#     return render(request, 'creativemanagement/upload1.html')
def upload(myfile,id):
    fs = FileSystemStorage()
    print("fs",fs)
    filename = fs.save(myfile.name, myfile)
    url = fs.url(myfile)
    print(url)
    bucket_name = 'creativemanagement-truecoverage'
    local_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(local_folder_path)
    local_file_path=local_folder_path+url
    print(local_file_path)
    s3_key = filename
    upload_to_s3(local_file_path, bucket_name, s3_key)
    print("uploaded")

    creative = Creative.objects.get(id=id)
    creative.status="uploaded"
    creative.file_object_name=s3_key
    creative.save() 

    # local_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # local_file_path=local_folder_path+url
    # print("localpath",local_file_path)
    # if settings.USE_S3:
    #     upload = UploadPrivate(file=myfile)
    # upload.save()
    # myfile_url = upload.file.url
    # print(myfile_url)
    # print("filesaved")





def ajax(request):
    if request.method == 'POST':
        creativeName=request.POST.get('creativeName')
        creator=request.POST.get('creator')
        lob=request.POST.get('lob')
        creativeType=request.POST.get('creativeType')
        platform=request.POST.get('platform')
        myfile = request.FILES['file']
        myfile_name = request.FILES['file'].name
        print(platform)

        id="1"
        creative = Creative(id=id,name=creativeName,
        creator=creator,lob=lob,creative_type=creativeType,
        platform=platform,file_object_name="--",status="Uploading")        
        creative.save()

        # fs = FileSystemStorage()
        # print("fs",fs)
        # filename = fs.save(myfile.name, myfile)

        # if settings.USE_S3:
        #     upload = UploadPrivate(file=myfile)
        # upload.save()
        # myfile_url = upload.file.url
        startTreading = threading.Thread(target=uploadmulti,args=(myfile,myfile_name),daemon=True)
        startTreading.start()
        return JsonResponse({'data': 'success'})
    else:
        ajax_list = []
        context = {'ajax_list': ajax_list}
    return render(request, 'creativemanagement/upload.html', {'ajax_list': ajax_list})
    # return render(request, 'tc_DigitalMarketing/test_upload.html')

















from django.core.files.storage import default_storage

def save_video_in_thread(file_data, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Open the file and save the data in chunks
    with default_storage.open(file_path, 'wb') as destination:
        for chunk in file_data.chunks():
            destination.write(chunk)


# Assuming you have a view where you receive the file data
def my_video_upload_view(request):
    if request.method == 'POST' and request.FILES.get('video'):
        file_data = request.FILES['video']
        file_name = file_data.name

        # Create and start a new thread to save the file
        thread = threading.Thread(target=save_video_in_thread, args=(file_data, file_name))
        thread.start()

        return HttpResponse('Video is being saved in a separate thread.')
    return render(request, 'creativemanagement/upfile.html')
