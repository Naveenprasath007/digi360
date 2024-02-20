from celery import shared_task
import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
import json
import base64
from django.conf import settings

@shared_task(bind=True)
def process_uploaded_file(self,file_data,filename):
    # File path on the server
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Write file data to the server
    # with open(file_path, 'wb') as f:
    #     f.write(file_data)
    
    with open(file_path, 'wb') as f:
            f.write(file_data)


# @shared_task(bind=True)
# def uploadfil(data):
#     byte_data = data['content_base64'].encode(encoding='utf-8')
#     b = base64.b64decode(byte_data)


@shared_task(bind=True)
def upload_to_s3_and_save(self,file_content,file_name):
    fs = FileSystemStorage()
    filename = fs.save(file_content.name, file_content)
    # # temp_dir = '/tmp/'
    # temp_dir = tempfile.mkdtemp()
    # temp_file_path = os.path.join(temp_dir, file_name)
    
    # # Save the file content to the temporary location
    # with open(temp_file_path, 'wb') as f:
    #     f.write(file_content)
    # os.remove(temp_file_path)
    # print('temp_file_path',temp_file_path)


@shared_task(bind=True)
def upload_to_s3_and_save_chunk(self,chunk, chunk_number, total_chunks, file_name, bucket_name, s3_key):
    # Define the temporary directory to save the chunk
    temp_dir = tempfile.mkdtemp()
    temp_chunk_path = os.path.join(temp_dir, f'{file_name}.part{chunk_number}')
    print(temp_dir)

    # Save the chunk to the temporary location
    with open(temp_chunk_path, 'wb') as f:
        f.write(chunk)
    
    # Check if all chunks have been uploaded
    if chunk_number == total_chunks:
        # Concatenate all chunks into the final file
        with open(temp_chunk_path, 'ab') as final_file:
            for i in range(1, total_chunks + 1):
                chunk_path = os.path.join(temp_dir, f'{file_name}.part{i}')
                with open(chunk_path, 'rb') as chunk_file:
                    final_file.write(chunk_file.read())
                os.remove(chunk_path)
        
        # Upload the final file to S3
        # s3 = boto3.client('s3')
        # with open(temp_chunk_path, 'rb') as final_file:
        #     s3.upload_fileobj(final_file, bucket_name, s3_key)
        
        # Delete the temporary file after upload
        os.remove(temp_chunk_path)
