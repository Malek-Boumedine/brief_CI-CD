from sqlmodel import Session
from utils import bcrypt_context
from sqlmodel import SQLModel
from database import engine
from modeles import Users
import os
from dotenv import load_dotenv, find_dotenv


dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path, override=True)

API_USER = os.getenv("API_USER", "admin")
API_EMAIL = os.getenv("API_EMAIL", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "admin")


def populate_db():

    with Session(engine) as session:
        
        # Ajouter un utilisateur admin
        admin_user = Users(
            username=API_USER,
            email=API_EMAIL,
            hashed_password=bcrypt_context.hash(API_PASSWORD),
            is_admin=1)
        session.add(admin_user)
        session.commit()
        print("✅ Utilisateur admin ajouté avec succès")
    
if __name__ == "__main__" :
    
    SQLModel.metadata.create_all(engine)
    populate_db()
