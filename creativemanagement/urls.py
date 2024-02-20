from django.contrib import admin
from django.urls import path
from creativemanagement import views
from django.contrib.auth import views as auth_views


urlpatterns = [
        path('getajax/', views.getajax, name='getajax'),
        path('ajax/', views.ajax, name='ajax'),
        path('upload/',views.upload_file, name='upload_file'),
        path('uploadnew/',views.my_video_upload_view, name='upload_file'),
        path('save-upload-info/', views.save_upload_info, name='save_upload_info'),
        path('',views.index,name='index'),
        path('fileview/<str:id>',views.fileview,name="fileview")
]
  