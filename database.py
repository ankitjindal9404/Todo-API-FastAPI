#1) Imports
import pymysql
pymysql.install_as_MySQLdb()
import os #to acess environement variable
from dotenv import load_dotenv #import the load_dotenv function to loads variables from .env file.
# from urllib.parse import quote_plus #If your password has symbols like @, $, /, etc., quote_plus() makes it safe to use in a URL so your database connection won't break.
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#2) Load Environement Variable
load_dotenv() #load environment variable from the .env file.

#3) Fetch Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL") #Get the DATABASE_URL environement variable and store it in variable DATABASE_URL

#4) Create database engine (connection): connects Python code to the MySQL database.
engine = create_engine(DATABASE_URL) #Creating engine to act as bridge btween code and database.

#5) Create metadata object
metadata = MetaData() #To hole info about tables, columns, constraints, etc.-basically DB schema

#6) Create session factory
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#7) Define base class for models
Base = declarative_base() #Base is the base class you’ll use to create your database models (tables) as Python classes.

#8) Summary
# This file sets up the foundation for:
    # Connecting your app to a MySQL DB
    # Writing table models
    # Running SQL queries from Python using SQLAlchemy
    # You're now ready to define models and start interacting with the database.