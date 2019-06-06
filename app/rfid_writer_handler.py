from socket import socket, SOCK_STREAM, AF_INET
import time

class RfidWriterTcpClient:
    def __init__(self,af_inet,port):
        self.af_inet=af_inet
        self.port=port
    def set_writer_addr(self,ip,port):
        self.af_inet=ip
        self.port=port
    def send_uid(self,uid):
        self.s=socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.af_inet,self.port))
        self.s.sendall(bytes.fromhex(uid))
        data=self.s.recv(1024).decode("utf-8").split(",")
        self.s.close()
        return data
