from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
from modeles import *



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URLl", "sqlite:///./api_users.db")

print(DATABASE_URL)

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine) 

def db_connection():
    session = Session(engine)  
    try:
        yield session  
    finally:
        session.close()  
        
        
        
        