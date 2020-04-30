ESP8266 RFID Lock System
==========================

An RFID Lock system with an esp8266 on micropython and a flask back end.

**NOTE** This project is not production ready and secure, its meant to be a learning material.

# Installation

```
git clone https://github.com/jakhax/esp9266_rfid_lock/
```

### Creating a virtual environment
```bash
sudo apt-get install python3.6-venv
python3.6 -m venv virtual
source virtual/bin/activate
pip install -r requirements.txt
pip install -r requirements-esp32.txt
```

## Install firmware on ESP866/ESP32 with Micropython


 See the following resources to get started and install micropython.
 
 
 - [https://docs.micropython.org/en/latest/esp8266/tutorial/](https://docs.micropython.org/en/latest/esp8266/tutorial/)
 - [GETTING STARTED WITH MICROPYTHON ON ESP8266](https://medium.com/@jackogina60/getting-started-with-micropython-on-esp8266-32eba914fed2)


### get python usb repl.
 - you require picocom for this, `sudo apt install picocom`
 ```bash
 picocom -b 115200 /dev/ttyUSB0
 ```

 ### deploy rfid reader code 
 ```bash
 ampy --port /dev/ttyUSB0 put reader/lock.py
 ampy --port /dev/ttyUSB0 put reader/mfrc522.py
 ampy --port /dev/ttyUSB0 put reader/main.py
 ```

  ### deploy rfid writers code 
 ```bash
 ampy --port /dev/ttyUSB0 put reader/_server.py
 ampy --port /dev/ttyUSB0 put reader/mfrc522.py
 ampy --port /dev/ttyUSB0 put reader/main.py
 ```

## Flask Server

### Setup DB

Create Database preferably on postgres, then add its url to `config.py` or set it as a env variable  `DATABASE_URL`

Run migrations `python manage.py db migrate`

### Running in development
```bash
python manage.py runserver
```
Open the app on your browser, by default on `127.0.0.1:5000`.


## References
- [https://docs.micropython.org/en/latest/esp32/tutorial/intro.html](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

## License ##
This project is licensed under the MIT Open Source license.
