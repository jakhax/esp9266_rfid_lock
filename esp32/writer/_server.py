import socket,sys
from os import uname
import time
import network
from mfrc522 import MFRC522

class TcpServer:
    sleep_time=2
    wifi_ssid="Moringa-Student"
    wifi_password="@#learn2017"
    server_url="http://20.20.22.58:5000/validate-pin"
    rc522_pins={"sck":18,"mosi":23,"miso":19,"rst":22,"sda":21}
    rc522_uid_addr=0x08
    
    def __init__(self,af_inet,port):
        if uname()[0] == 'esp32':
            pass
        else:
            raise RuntimeError("Wrong Platform")
        self.init()
        self.af_inet=af_inet
        self.port=port
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            sys.exit("Socket creation error: " + str(msg))
        self.init()

    def init(self):
        self.create_rc522()

    def create_rc522(self):
        self.rc522=MFRC522(
            self.rc522_pins["sck"],self.rc522_pins["mosi"],self.rc522_pins["miso"],
            self.rc522_pins["rst"],self.rc522_pins["sda"]
        )
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

    def set_wifi_conf(self,ssid,password):
        self.wifi_ssid=ssid
        self.wifi_password=password

    def get_wifi_conf(self):
        return self.wifi_ssid,self.wifi_password

    def connect_to_wifi(self):
        sta_if=network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.wifi_ssid,self.wifi_password)
        while sta_if.isconnected==False:
            pass

    def terminate_socket(self):
        try:
            self.s.close()
        except Exception as err:
            print("ERROR:"+err)

    def socket_bind(self):
        try:
            print("Binding socket to port: " + str(self.port))
            self.s.bind((self.af_inet,self.port))
            self.s.listen(5)
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
            try: self. terminate_socket()
            except Exception as err: print("ERROR:"+str(err))
            self.socket_bind()

    def receive_commands(self):
        while True:
            conn, address = self.s.accept()
            print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
            data=conn.recv(1024)
            if data: 
                if len(data)!=16:
                    conn.send("Invalid data length".encode("utf-8"))
                    conn.close()
                else:
                    try: 
                        print(data)
                        print("\nPlace rfid tag near the reader to write to it\n")
                        while True:
                            (stat, tag_type) = self.rc522.request(self.rc522.REQIDL)
                            if stat == self.rc522.OK:
                                (stat, raw_uid) = self.rc522.anticoll()
                                if stat == self.rc522.OK:
                                    print("New card detected")
                                    print("  - tag type: 0x%02x" % tag_type)
                                    print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                                    print("")
                                    if self.rc522.select_tag(raw_uid) == self.rc522.OK:
                                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                                        if self.rc522.auth(self.rc522.AUTHENT1A, self.rc522_uid_addr, key, raw_uid) == self.rc522.OK:
                                            stat = self.rc522.write(self.rc522_uid_addr, data)
                                            self.rc522.stop_crypto1()
                                            if stat == self.rc522.OK:
                                                print("Data written to card")
                                            else:
                                                print("Failed to write data to card")
                                        else:
                                            print("Authentication error")
                                    else:
                                        print("Failed to select tag")
                                    break
                        response="success"
                        conn.send(response.encode("utf-8"))
                        conn.close()
                    except Exception as err:
                        print("ERROR:%s"%err)
                        conn.close()
                        pass
            else:
                conn.close()
                pass  
                