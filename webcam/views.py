from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .videobase import VideoDemo, VideoApp, VideoBase


pk = -1
cap = VideoBase()

@csrf_protect
def Init(request):
    global pk 
    global cap
    if request.method == 'GET':
        pk = request.GET.get('pk')
        print("pk = ",pk)
        if pk == '0':
            cap = VideoDemo()
        else:
            cap = VideoApp()
        return JsonResponse({"result":pk})

@csrf_protect
def connect(request):
    if request.method == 'GET':
        cap.connect()
        return JsonResponse({ "result":"connect sucssed!"})


@csrf_protect
def disconnect(request):
    if request.method == 'GET':
        cap.disconnect()
        return JsonResponse({ "result":"disconnect sucssed!"})

@csrf_protect
def video_feed(request):
    return StreamingHttpResponse(cap.stream(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_protect
def capture(request):
    name, box = cap.capture()
    return JsonResponse({ "name":name})


def home(request):
    return render(request, 'index.html', {'ListStudent': cap.listStudent(pk), 'update':'True', 'pk':pk})



##############################################################
