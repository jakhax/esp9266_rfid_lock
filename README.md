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
- @todo document
## Technology used

* [Python3.6](https://www.python.org/)

## References
- @todo document

## Known Bugs 

There are no known bugs. If you find any be sure to create an issue 

## License ##
This project is licensed under the MIT Open Source license.