from lib.imqttdriver import IMqttDriver
import paho.mqtt.client as mqtt
class AzureDriver(IMqttDriver):
    """Azure Driver"""
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
