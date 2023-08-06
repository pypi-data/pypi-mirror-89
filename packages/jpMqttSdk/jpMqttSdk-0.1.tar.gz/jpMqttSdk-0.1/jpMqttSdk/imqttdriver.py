import paho.mqtt.client as mqtt
class IMqttDriver():
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'on_message') and 
                callable(subclass.on_message) and 
                hasattr(subclass, 'on_connect') and 
                callable(subclass.on_connect) and 
                hasattr(subclass, 'connect') and 
                callable(subclass.connect) and 
                hasattr(subclass, 'on_publish') and 
                callable(subclass.on_publish) and   
                hasattr(subclass, 'publish') and 
                callable(subclass.publish) and  
                hasattr(subclass, 'osubscribe') and 
                callable(subclass.subscribe) and                
                hasattr(subclass, 'on_subscribe') and 
                callable(subclass.on_subscribe) or 
                NotImplemented)

    
  
    def connect(self):
        """On connection request"""
        raise NotImplementedError

    def on_connect(self,Client:mqtt.Client, userdata:str, flags, rc):
        """On Conncetion established"""
        raise NotImplementedError

    def publish(self,Client:mqtt.Client,topic,payload):
        """On publish Request"""
        raise NotImplementedError

    def on_publish(self,Client:mqtt.Client, obj, mid):
        """On published"""
        raise NotImplementedError

    def subscribe(self,topic,qos):
        """On Subscribe request"""
        raise NotImplementedError

    def on_subscribe(self,Client:mqtt.Client, obj, mid, granted_qos):
        """On subscribed"""
        raise NotImplementedError
    def on_message(self,Client:mqtt.Client, obj, msg):
        """On message Recived"""
        raise NotImplementedError