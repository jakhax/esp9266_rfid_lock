from _server import TcpServer

def main():
    writer=TcpServer("0.0.0.0",9999)
    writer.set_wifi_conf("GOT","MASTER2D")
    writer.connect_to_wifi()
    writer.set_rc522_uid_addr(0x08)
    writer.socket_bind()
    while True:
        writer.receive_commands()
    writer.terminate_socket()

if __name__=="__main__":
    main()