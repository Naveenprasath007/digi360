from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import threading
from django.core.files.storage import FileSystemStorage
from .models import Creative
import os
import boto3
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# from aiohttp import web
# import asyncio




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


def uploadmulti(file_data,filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)







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
        # file_content = request.FILES['file']
        uploaded_file = request.FILES['file'].read()
        uploaded_name= request.FILES['file'].name
        # serialize_video_file.delay(uploaded_file,file_content)
        # serialize_video_file(uploaded_file,file_content)
        uploaded_name= request.FILES['file'].name
        startTreading = threading.Thread(target=uploadmulti,args=(uploaded_file,uploaded_name),daemon=True)
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


def getajax(request):
    if request.method == 'GET':
        if Creative(request):
            # data = Creative.objects.order_by('-created_at').first()
            data = Creative.objects.all()
            print(data)
            # created = data.created_at.strftime('%m-%d-%Y %H:%M:%S')
            datas = {"id": "1", "text": "data.text", "search": "data.search", "email": "naaa",
                     "telephone": "data.telephone", "created_at": "created"}

            return JsonResponse(datas)
    else:
        return JsonResponse({'data': 'failure'})


def ajax(request):
    if request.method == 'POST':
        creativeName=request.POST.get('creativeName')
        creator=request.POST.get('creator')
        lob=request.POST.get('lob')
        creativeType=request.POST.get('creativeType')
        platform=request.POST.get('platform')
        myfile = request.FILES['file']
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
        startTreading = threading.Thread(target=upload,args=(myfile,id),daemon=True)
        startTreading.start()
        return JsonResponse({'data': 'success'})
    else:
        ajax_list = []
        context = {'ajax_list': ajax_list}
    return render(request, 'creativemanagement/upload.html', {'ajax_list': ajax_list})
    # return render(request, 'tc_DigitalMarketing/test_upload.html')