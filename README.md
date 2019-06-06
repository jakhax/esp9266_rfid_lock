Consecutive normal punches
==========================


# Installation

## Flask Server

### Requirements
* Python 3.6.5
* micropython

### Cloning the repository
```bash
git clone repo-link && cd repo-dor
```

### Creating a virtual environment
```bash
sudo apt-get install python3.6-venv
python3.6 -m venv virtual
source virtual/bin/activate
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python manage.py test
```

### Create admin / superuser
```bash
python manage.py createsuperuser
```

### Running in development
```bash
python manage.py runserver
```
Open the app on your browser, by default on `127.0.0.1:5000`.

### Deploying to heroku
- @todo document

## Esp32
- I have written some shell scripts to enable you to easily write flash, upload and remove files from the board.

### Installing dependencies
```bash
pip install -r requirements-esp32.txt
```

### write flash

```bash
cd esp32
./write_fash.sh esp32-20190604-v1.11-25-gce8262a16.bin
```

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

## Technology used

* [Python3.6](https://www.python.org/)

## References
- [https://docs.micropython.org/en/latest/esp32/tutorial/intro.html](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

## Known Bugs 

There are no known bugs. If you find any be sure to create an issue 

## License ##
This project is licensed under the MIT Open Source license.