# Generated by Django 4.1.7 on 2024-02-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creativemanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creative',
            name='status',
            field=models.CharField(default=(2016, 7, 7, 9, 11, 6, 489063), max_length=100),
            preserve_default=False,
        ),
    ]
