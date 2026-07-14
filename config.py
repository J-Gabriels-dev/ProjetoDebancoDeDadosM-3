import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "sistema-licenca-dev")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:Jgpds28%25@localhost/sistema_licenca_capacitacao",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
