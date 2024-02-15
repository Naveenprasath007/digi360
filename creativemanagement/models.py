from django.db import models

class Creative(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    lob = models.CharField(max_length=100)
    creative_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    file_object_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name