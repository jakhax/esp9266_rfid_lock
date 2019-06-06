import os

class Config:
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL","postgres+psycopg2://postgres:p@127.0.0.1:5432/lock")
    SECRET_KEY=os.environ.get("SECRET_KEY","super secret key")

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