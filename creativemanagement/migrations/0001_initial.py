# Generated by Django 4.1.7 on 2024-02-19 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creative',
            fields=[
                ('id', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100)),
                ('lob', models.CharField(max_length=100)),
                ('creative_type', models.CharField(max_length=100)),
                ('platform', models.CharField(max_length=100)),
                ('file_object_name', models.URLField(max_length=1024)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_location', models.URLField(max_length=1024)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
