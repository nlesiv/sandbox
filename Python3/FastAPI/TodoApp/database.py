from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

username = os.getenv("DB_USER")
password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todoapp.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@mysqlserver/db"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()