import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
 
MQTT_SERVER = "192.168.1.5"
MQTT_PATH = "msgChannel04"
 



GPIO.setmode(GPIO.BCM)

GPIO.setup(24,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

Motor1 = GPIO.PWM(25, 50)
Motor1.start(0)
Motor2 = GPIO.PWM(11, 50)
Motor2.start(0)

def forward(speed):
  GPIO.output(24,GPIO.HIGH)
  GPIO.output(23,GPIO.LOW)
  GPIO.output(9,GPIO.HIGH)
  GPIO.output(10,GPIO.LOW)
  Motor1.ChangeDutyCycle(speed)
  Motor2.ChangeDutyCycle(speed)

def backward(speed):
  GPIO.output(24,GPIO.LOW)
  GPIO.output(23,GPIO.HIGH)
  GPIO.output(9,GPIO.LOW)
  GPIO.output(10,GPIO.HIGH)
  Motor1.ChangeDutyCycle(speed)
  Motor2.ChangeDutyCycle(speed)

def left(speed):
  GPIO.output(24,GPIO.HIGH)
  GPIO.output(23,GPIO.LOW)
  Motor1.ChangeDutyCycle(speed)

def right(speed):
  GPIO.output(9,GPIO.HIGH)
  GPIO.output(10,GPIO.LOW)
  Motor2.ChangeDutyCycle(speed)

def stop():
  Motor1.ChangeDutyCycle(0)
  Motor2.ChangeDutyCycle(0)

#forward(50)
#sleep(3)
#backward(50)
#sleep(10)
#forward(50)
#sleep(5)
#stop()
#left(75)
#sleep(2)
#right(75)
#sleep(2)
#stop()
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	forward(50)
	sleep(6)
	stop()
# more callbacks, etc
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

GPIO.cleanup()