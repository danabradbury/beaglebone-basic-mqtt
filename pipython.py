import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread
import psutil
            
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
    print("on_disconnect callback "+str(rc))
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("on_publish callback "+str(mid))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.tls_set(ca_certs='./AmazonRootCA1.pem', certfile='./4cdeb7d5ccc7652a22a872ca4a70517c797b02491af17210166aeffd6edbccdb-certificate.pem.crt', keyfile='./4cdeb7d5ccc7652a22a872ca4a70517c797b02491af17210166aeffd6edbccdb-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3ladch462vwid-ats.iot.us-east-1.amazonaws.com", 8883, 60) #Taken from REST API endpoint - Use your own. 

def intrusionDetector(Dummy):
    while (1):    
        if (1): 
            message_json = json.dumps(
            	{
            		"time": int(time.time() * 1000),
            		"quality": "GOOD",
            		"hostname": "beagle",
            		"value": psutil.cpu_percent(),
            	}, indent=2)
            print("sending payload to aws: ", message_json)
            client.publish("home/monitor", payload=message_json , qos=0, retain=False)
        time.sleep(60)

thread.start_new_thread(intrusionDetector,("Create intrusion Thread",))
    
client.loop_forever()   