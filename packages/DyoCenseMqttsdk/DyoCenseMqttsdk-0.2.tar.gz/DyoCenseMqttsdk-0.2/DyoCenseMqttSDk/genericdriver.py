import paho.mqtt.client as mqtt
import urllib.parse
import ssl
import time
import threading 
from datetime import datetime
import random
import json
from lib.imqttdriver import IMqttDriver

class GenricDriver(IMqttDriver):
    """Genric Driver."""
    mqttc:mqtt.Client=None
    clientId=''
    def connect(self,url:str,enableSSl:bool,serialNumber:str,deviceSku:str,certs_req:None,certfile:str):
        """On connection request"""
        print("connection request")        
       
        self.clientId = deviceSku+'/'+serialNumber
        username = self.clientId
        password = serialNumber

        self.mqttc = mqtt.Client(client_id= self.clientId, clean_session=True)

        # Assign event callbacks

        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe =self.on_subscribe

        url_str = url
      
        url = urllib.parse.urlparse(url_str)
     
        # Connect
        self.mqttc.enable_logger()
        if enableSSl:
            if certs_req:
                self.mqttc.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2,certfile=certfile)
            else:
                self.mqttc.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

        self.mqttc.username_pw_set(username, password)
        self.mqttc.connect(url.hostname, url.port,  keepalive=60)
        self.mqttc.loop_forever()     
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
       

      

    def on_connect(self,client, userdata:str, flags, rc):
        """On Conncetion established"""
        print("connected successfully")
        topic = self.clientId+'/twin/credentials/PATCH/#'
        qos = 0      
        self.subscribe(topic,qos)
        print('subscribed to defults') 

       

    def publish(self,client,topic,payload):
        """On publish Request"""
        print("publishing ")
        

    def on_publish(self,client, obj, mid):
        """On published"""
        print("published ")
        

    def subscribe(self,topic,qos):
        """On Subscribe request"""
        self.mqttc.subscribe([(topic, qos)]) 
        
       

    def on_subscribe(self,client, obj, mid, granted_qos):
        """On subscribed"""
        print("subscribed with Mid " +mid +" with qos " + granted_qos)
       
    def on_message(self,client, obj, msg):
        """On message Recived"""
        print(msg)
       
