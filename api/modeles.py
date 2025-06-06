from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, String



# class Users(SQLModel, table=True): 
#     id : Optional[int] = Field(default=None, primary_key=True, index=True)
#     username : str = Field(sa_column=Column(String(255), unique=True))
#     email: str = Field(sa_column=Column(String(255), unique=True))
#     hashed_password: str = Field(sa_column=Column(String(255)))
#     is_admin: bool = Field(default=0)


class Users(SQLModel, table=True):
    __tablename__ = 'users'  # spécifiez explicitement le nom de la table
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(sa_column=Column(String(255), unique=True))
    email: str = Field(sa_column=Column(String(255), unique=True))
    hashed_password: str = Field(sa_column=Column(String(255)))
    is_admin: bool = Field(default=False)

    # Ajoutez extend_existing=True ici si la table existe déjà
    __table_args__ = {'extend_existing': True}


