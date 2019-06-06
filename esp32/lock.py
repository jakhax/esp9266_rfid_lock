import machine
import urequests
import time
import network

class Lock:
    sleep_time=2
    wifi_ssid="Moringa-Student"
    wifi_password="@#learn2017"
    server_url="http://20.20.22.58:5000/validate-pin"
    
    def __init__(self,):
        self.built_in_led_pin=machine.Pin(2,machine.Pin.OUT)
        self.built_in_led_pin.value(0)

    def set_server_url(self,url):
        self.server_url=url

    def get_server_url(self):
        return self.server_url

    def set_sleep_time(self,time):
        self.sleep_time=time

    def get_sleep_time(self):
        return self.sleep_time

    def set_wifi_conf(self,ssid,password):
        self.wifi_ssid=ssid
        self.wifi_password=password

    def get_wifi_conf(self):
        return self.wifi_ssid,self.wifi_password

    def input_pin(self,id,pin):
        res=self.send_request({"id":id,"pin":pin})
        if res:
            if res["response"]==True:
                self.built_in_led_pin.value(1)
                time.sleep(self.sleep_time)
                self.built_in_led_pin.value(0)
            else:
                time.sleep(self.get_sleep_time)
                print("wrong pin or id")
        else:
            print("Error occured, try again")

    def send_request(self,data):
        res=urequests.post(self.server_url,json=data)
        if res.status_code==200:
            print(res.json())
            return res.json()
        else:
            return False

    def connect_to_wifi(self):
        sta_if=network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.wifi_ssid,self.wifi_password)
        while sta_if.isconnected==False:
            pass
        

