from lock import Lock

def main():
    lock=Lock()
    lock.set_server_url("http://192.168.0.17:5000/validate-pin")
    lock.set_wifi_conf("GOT","MASTER2D")
    lock.connect_to_wifi()
    lock.set_rc522_uid_addr(0x08)
    lock.run()
if __name__=="__main__":
    main()