from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.generic import ListView
from .models import Student
from django.http import JsonResponse
# from rest_framework import  serializers
from django.views.decorators.csrf import csrf_protect
def attend(request):
    return render(request, 'attend.html')

def stream():
    cap = App()
    cap.aws_connect('Python_Client')
    while True:
        try:
            message = cap.gui_queue.get_nowait()
        except queue.Empty:
            message = None
        if message is not None:
            _image = message.get("Image")
            _image.save('media/cam3.png', format="PNG")
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('media/cam3.png', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_protect
def capture(request):
    #  load model 
    if request.method == 'GET':
        ListStudent = Student.objects.all() 
        for student in ListStudent:
            student.status = 0
            student.save()
  
        capture = "Pham Quoc Viet"
        print("get get get")
        return JsonResponse({ "capture":capture})


class ListStudent(ListView):
    queryset = Student.objects.all()
    template_name = 'index.html'
    context_object_name = 'ListStudent'

############################################################################################################
################################################################################
import io
import queue
import traceback
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from PIL import Image

class App:
    def __init__(self):
        self.myAWSIoTMQTTClient = None
        self.gui_queue = queue.Queue()
        self.u = 0    
    def aws_connect(self, client_id):
        ENDPOINT = "a6qz2b7pn3k7l-ats.iot.us-east-1.amazonaws.com"
        PATH_TO_CERT = "certificates/DeviceCertificate.crt"
        PATH_TO_KEY = "certificates/Private.key"
        PATH_TO_ROOT = "certificates/RootCA.pem"

        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

        try:
            if self.myAWSIoTMQTTClient.connect():
                self.add_note('[MQTT] Connected')
                for i in range(1):
                    self.mqtt_subscribe('esp32/cam_{}'.format(i))

            else:
                self.add_note('[MQTT] Cannot Access AWS IOT')
        except Exception as e:
            tb = traceback.format_exc()
            print(f'An error happened.  Here is the info:', e, tb)        
    def aws_disconnect(self):
        if self.myAWSIoTMQTTClient is not None:
            self.myAWSIoTMQTTClient.disconnect()
            self.add_note('[MQTT] Successfully Disconnected!')  
   
    def mqtt_subscribe(self, topic):
        if self.myAWSIoTMQTTClient.subscribe(topic, 0, lambda client, userdata, message: {

            self.gui_queue.put({"Image": self.byte_image_to_png(message)})
        }):
            self.add_note('[MQTT] Topic: {}\n-> Subscribed'.format(topic))
        else:
            self.add_note('[MQTT] Cannot subscribe\nthis Topic: {}'.format(topic))  

    def add_note(self, note):
        print(note)

    def byte_image_to_png(self, message):
        print(self.u)
        self.u+=1
        bytes_image = io.BytesIO(message.payload)
        picture = Image.open(bytes_image)
        return picture