from django.db import models

class Creative(models.Model):
    id = models.CharField(max_length=225,primary_key=True)
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    lob = models.CharField(max_length=100)
    creative_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    file_object_name = models.URLField(max_length=1024)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
class UploadInfo(models.Model):
    file_name = models.CharField(max_length=255)
    file_location = models.URLField(max_length=1024)
    upload_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name