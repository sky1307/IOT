import paho.mqtt.client as mqtt
import time
import io
import base64
from PIL import Image
import cv2
import numpy as np
import pygame

img_received = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/cam_0")

def on_message(client, userdata, message):
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	img = base64.decodebytes(message.payload)
	global img_received
	img_received = True
	with open("imageToSave.jpg", "wb") as fh:
		fh.write(img)

if __name__ == '__main__':
	display_width = 800
	display_height = 600

	gameDisplay = pygame.display.set_mode((display_width,display_height))
	pygame.display.set_caption('MQTT Subscriber')
  
	# activate the pygame library . 
	# initiate pygame and give permission 
	# to use pygame's functionality. 
	pygame.init() 

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("192.168.1.68", 1883)
	client.loop_start()
	#time.sleep(0.1) # wait
	while True:
		try:
			if img_received:
				print("Image received")
				img_received = False
				carImg = pygame.image.load("imageToSave.jpg")
				gameDisplay.blit(carImg, (0,0))
		except Exception as e:
			print(e)
		pygame.display.update()
	client.loop_stop() #stop the loop