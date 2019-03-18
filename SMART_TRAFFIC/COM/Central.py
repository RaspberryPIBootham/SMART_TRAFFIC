import paho.mqtt.publish as publish 
MQTT_SERVER = "192.168.1.5"
MQTT_PATH = "msgChannel01"
DETECT_MESSAGE="Car detected on Lane 01"
publish.single(MQTT_PATH, DETECT_MESSAGE, hostname=MQTT_SERVER)

MQTT_PATH2 = "msgChannel02"
DETECT_MESSAGE2="Car detected on Lane 02"
publish.single(MQTT_PATH2, DETECT_MESSAGE2, hostname=MQTT_SERVER)


MQTT_PATH3 = "msgChannel03"
DETECT_MESSAGE3="Car detected on Lane 03"
publish.single(MQTT_PATH3, DETECT_MESSAGE3, hostname=MQTT_SERVER)


MQTT_PATH4 = "msgChannel04"
DETECT_MESSAGE4="Car detected on Lane 04"
publish.single(MQTT_PATH4, DETECT_MESSAGE4, hostname=MQTT_SERVER)

