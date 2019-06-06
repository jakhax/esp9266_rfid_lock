import os
from socket import socket, SOCK_STREAM, AF_INET
import time

class RfidWriterTcpClient:
    af_inet=os.getenv("RFID_WRITER_IP",default="192.168.0.30")
    port=int(os.getenv("RFID_WRITER_PORT",default=9999))

    def __init__(self):
        pass

    def set_writer_addr(self,ip,port):
        self.af_inet=ip
        self.port=port

    def send_uid(self,uid):
        self.s=socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.af_inet,self.port))
        self.s.sendall(bytes.fromhex(uid))
        data=self.s.recv(1024).decode("utf-8")
        self.s.close()
        return data
