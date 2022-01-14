from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.generic import ListView
from .models import Student
from django.http import JsonResponse
# from rest_framework import  serializers
import cv2
from django.views.decorators.csrf import csrf_protect
def attend(request):
    return render(request, 'attend.html')

def stream():
    cap = cv2.VideoCapture(cv2.CAP_V4L2) 

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('media/cam.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('media/cam.jpg', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_protect
def capture(request):
    #  load model 
    if request.method == 'GET':
        # ListStudent = Student.objects.all() 
        # for student in ListStudent:
        #     student.status = 1
        #     student.save()
        # ListStudent = serializers.serialize('json', ListStudent, fields=("id", "name", "mssv", "Class","status"))
        capture = "Pham Quoc Viet"
        print("get get get")
        return JsonResponse({ "capture":capture})


class ListStudent(ListView):
    queryset = Student.objects.all()
    template_name = 'index.html'
    context_object_name = 'ListStudent'

