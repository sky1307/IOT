import queue
import time
from .tasks import face_ai
from .models import Student
import paho.mqtt.client as mqtt
import time
import base64



class VideoBase():
    def __init__(self):
        self.Class = "-1"
        self.queue = queue.Queue()
        self.start_time = time.time()
        self.con = False
    
    def connect(self):
        self.con = True
        self.note("connect . .  .")
        self.note("connect successfully!")
        return True 
    def disconnect(self):
        self.con = False
        self.note("disconnect . .  .")
        self.note("disconnect successfully!")
        return True

    def capture(self):
        self.test_DB()
        return "Viet Pham", [1,2,3,4]

    def stream(self):
        file_name ='media/demo.jpg'
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n') 

    def note(self, message):
        print(message)

    def listStudent(self, pk):
        return Student.objects.filter(Class=pk)

    def updateStudent(self,name, status):
        student = Student.objects.get(name=name, Class=self.Class)
        student.status = status 
        student.save()
    def test_DB(self):
        students = Student.objects.filter(Class=self.Class)
        print(self.Class)
        for std in students:
            std.status = 1-std.status
            std.save()

class VideoDemo(VideoBase):
    def __init__(self):
        super().__init__() 
        self.Class = "0"

    def stream(self):
        if self.con == False:
            file_name = "media/demo.jpg"
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
        else:
            j = 0
            while True:
                time.sleep(0.05)
                j = j%7 +1
                # print(j)
                file_name = 'media/HoangLong/'+str(j)+'.JPG'
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')       
        
    def capture(self):
        name, box= face_ai('media/demo.jpg') 
        self.note("get get get")
        self.test_DB()
        # if name != 'Unknown':
        #     # self.updateStudent(name, 1)
        return name, box

    
class VideoApp(VideoBase):
    def __init__(self):
        super().__init__() 
        self.Class = "1"
        self.img_received = False
        self.client = None
    
    def connect(self):
        self.con = True
        self.note("connect . .  .")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("192.168.1.68", 1883)
        self.client.loop_start()
        self.note("connect successfully!")
        return True 

    def disconnect(self):
        self.con = False
        self.client.loop_stop()
	
    def stream(self):
        if self.con == False:
            file_name = "media/demo.jpg"
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
        else:
            while True:
                try:
                    if img_received:
                        print("Image received")
                        img_received = False
                        file_name = "media/imageToSave.jpg"
                        yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
                except Exception as e:
                    print(e)


    def capture(self):
        name, box= face_ai('media/imageToSave.jpg') 
        self.note("get get get")
        self.test_DB()
        # if name != 'Unknown':
        #     # self.updateStudent(name, 1)
        return name, box

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("esp32/cam_0")

    def on_message(self, client, userdata, message):
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        img = base64.decodebytes(message.payload)
        self.img_received = True
        with open("media/imageToSave.jpg", "wb") as fh:
            fh.write(img)