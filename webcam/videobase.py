import queue
import time
from .tasks import face_ai
from .models import Student
import paho.mqtt.client as mqtt
import time
import base64
import cv2


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
        file_name = "media/background.png"
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
            file_name = "media/background.png"
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
        self.file_name = "media/imageToSave.png"
        self.file_output = "media/output.jpg"
        self.showbox = False
        self.current = 0
        self.c_capture = True
    
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
            file_name = "media/background.png"
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
        else:
            while True:
                if self.showbox == True:
                    yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_output, 'rb').read() + b'\r\n')
                    if time.time() - self.current > 2:
                        self.showbox = False
                        self.current = 0
                        self.c_capture = True
                else:
                    try:
                        if self.img_received:
                            print("Image received")
                            self.img_received = False

                            yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + self.payload  + b'\r\n')  #open(file_name, 'rb').read()
                    except Exception as e:
                        print(e)


    def capture(self):
        with open(self.file_name, "wb") as fh:
            fh.write(self.payload)
        if self.c_capture:
            self.c_capture = False
            name, box= face_ai(self.file_name) 
            self.note("get get get")
            self.test_DB()
            if len(name)!=0:
                self.showbox = True
                self.current = time.time()
            else:
                name.append("Unknown")
                self.c_capture = True
            return name, box
        else:
            return ['Waiting 2 second. . . .'], [] 
        
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("esp32/cam_0")

    def on_message(self, client, userdata, message):
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        img = base64.decodebytes(message.payload)
        self.payload = img
        self.img_received = True


################################################################
class WebCam(VideoBase):
    def __init__(self):
        super().__init__() 
        self.Class = "2"
        self.webcam = None
        self.file_name = "media/demo2.jpg"
        self.file_output = "media/output.jpg"
        self.showbox = False
        self.current = 0
        self.c_capture = True
       
    def disconnect(self):
        self.webcam.release() 
        self.webcam = None
        self.con = False
    def stream(self):
        if self.con == False:
            file_name = "media/background.png"
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open(file_name, 'rb').read() + b'\r\n')  
        else:
            self.webcam = cv2.VideoCapture(0) 
            while True:
                
                if self.showbox == True:
                    yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_output, 'rb').read() + b'\r\n')
                    if time.time() - self.current > 2:
                        self.showbox = False
                        self.current = 0
                        self.c_capture = True
                else:
                    ret, frame = self.webcam.read()

                    if not ret:
                        print("Error: failed to capture image")
                        break
                    cv2.imwrite(self.file_name, frame)
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + open(self.file_name, 'rb').read() + b'\r\n')


    def capture(self):
        if self.c_capture:
            self.c_capture = False
            name, box= face_ai(self.file_name) 
            self.note("get get get")
            self.test_DB()
            if len(name)!=0:
                self.showbox = True
                self.current = time.time()
            else:
                name.append("Unknown")
                self.c_capture = True
            return name, box
        else:
            return ['Waiting 2 second. . . .'], [] 