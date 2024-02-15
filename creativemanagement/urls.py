from django.contrib import admin
from django.urls import path
from creativemanagement import views
from django.contrib.auth import views as auth_views


urlpatterns = [
        path('getajax/', views.getajax, name='getajax'),
        path('ajax/', views.ajax, name='ajax'),
        path('upload',views.upload, name="upload"),
        path('save-video',views.save_video_view, name='save_video')
]