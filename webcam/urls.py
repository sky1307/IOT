from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListStudent.as_view(), name='ListStudent'),
    path('video_feed/', views.video_feed, name='video-feed'),
    path('capture/',views.capture, name='capture'),
]