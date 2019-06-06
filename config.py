import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY",default="super secret key")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL","postgres+psycopg2://postgres:p@127.0.0.1:5432/lock")

class DevConfig(Config):
    pass

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

config_options={
    "development":DevConfig,
    "production":ProdConfig,
    "test":TestConfig,
}