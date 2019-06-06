import machine
from os import uname
import urequests
import time
import network
from mfrc522 import MFRC522

class Lock:
    sleep_time=2
    wifi_ssid="Moringa-Student"
    wifi_password="@#learn2017"
    server_url="http://20.20.22.58:5000/validate-pin"
    rc522_pins={"sck":18,"mosi":23,"miso":19,"rst":22,"sda":21}
    rc522_uid_addr=0x08
    
    def __init__(self,):
        if uname()[0] == 'esp32':
            pass
        else:
            raise RuntimeError("Wrong Platform")
        self.init()

    def init(self):
        self.built_in_led_pin=machine.Pin(2,machine.Pin.OUT)
        self.built_in_led_pin.value(0)
        self.create_rc522()

    def create_rc522(self):
        self.rc522=MFRC522(
            self.rc522_pins["sck"],self.rc522_pins["mosi"],self.rc522_pins["miso"],
            self.rc522_pins["rst"],self.rc522_pins["sda"]
        )

    def set_server_url(self,url):
        self.server_url=url

    def get_server_url(self):
        return self.server_url

    def set_rc522_uid_addr(self,addr):
        self.rc522_uid_addr=addr
    
    def get_rc522_uid_addr(self):
        return self.rc522_uid_addr

    def set_rc522_pins(self,sck=18,mosi=23,miso=19,rst=22,sda=21):
        self.rc522_pins={
            "sck":sck,"mosi":mosi,"miso":miso,"rst":rst,"sda":sda
        }

    def get_rc522_pins(self):
        return self.rc522_pins

    def set_sleep_time(self,time):
        self.sleep_time=time

    def get_sleep_time(self):
        return self.sleep_time

    def set_wifi_conf(self,ssid,password):
        self.wifi_ssid=ssid
        self.wifi_password=password

    def get_wifi_conf(self):
        return self.wifi_ssid,self.wifi_password

    def send_request(self,data):
        try:
            res=urequests.post(self.server_url,json=data)
            if res.status_code==200:
                print(res.json())
                return res.json()
            else:
                return False
        except Exception as e:
            print("Error:",e)
            return False


    def connect_to_wifi(self):
        sta_if=network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.wifi_ssid,self.wifi_password)
        while sta_if.isconnected==False:
            pass

    def send_uid(self,uid):
        res=self.send_request({"uid":uid})
        if res:
            if res["response"]==True:
                self.built_in_led_pin.value(1)
                time.sleep(self.sleep_time)
                self.built_in_led_pin.value(0)
            else:
                time.sleep(self.get_sleep_time())
                print("wrong pin or id")
        else:
            print("Error occured, try again")
    
    def run(self):
        print("\nPlace card before reader to read from address {}\n".format(self.rc522_uid_addr))
        try:
            while True:
                (stat, tag_type) = self.rc522.request(self.rc522.REQIDL)
                if stat == self.rc522.OK:
                    (stat, raw_uid) = self.rc522.anticoll()
                    if stat == self.rc522.OK:
                        print("Card detected")
                        print("  - tag type: 0x%02x" % tag_type)
                        print("  - uid	 : 0x%02x%02x%02x%02x\n" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                        if self.rc522.select_tag(raw_uid) == self.rc522.OK:
                            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                            if self.rc522.auth(self.rc522.AUTHENT1A,self.rc522_uid_addr, key, raw_uid) == self.rc522.OK:
                                uid=self.rc522.read(self.rc522_uid_addr)
                                print("Address 8 data: %s" % uid)
                                self.rc522.stop_crypto1()
                                self.send_uid(uid)
                            else:
                                print("Authentication error")
                        else:
                            print("Failed to select tag")
        except KeyboardInterrupt:
                print("Exit..")
        

