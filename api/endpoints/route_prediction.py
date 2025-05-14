from fastapi import APIRouter, Depends
from typing import Annotated
from modele.main import charger_modele, prediction
from api.utils import get_current_user
from dotenv import load_dotenv
import os



load_dotenv()
chemin_modele = os.getenv("API_CHEMIN_MODEL", "../../src/complete_pipeline.pkl")


router = APIRouter()

@router.post("/predictions")
def get_predictions(data: dict,current_user: Annotated[str, Depends(get_current_user)]):
    pred = prediction(chemin_modele, data)
    
    return {
        "resultat de la prédiction" : pred
    }






