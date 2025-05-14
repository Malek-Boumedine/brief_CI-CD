import os
import sys
import pytest
from dotenv import load_dotenv
p_path = os.getcwd()
sys.path.append(p_path)
from modele.main import creer_exporter_modele, charger_modele, prediction



@pytest.fixture(scope="module")
def chemin_modele():
    return "src/modele_test.pkl"


def test_creer_exporter_modele(chemin_modele):
    message = creer_exporter_modele(chemin_modele)
    assert os.path.exists(chemin_modele), f"Le fichier {chemin_modele} est introuvable"
    assert isinstance(message, str)
    assert "exporté" in message


def test_charger_modele(chemin_modele):
    modele = charger_modele(chemin_modele)
    assert modele is not None
    assert hasattr(modele, "predict"), "Le modèle n'a pas de méthode predict()"
    
    
def test_prediction(chemin_modele) : 
    donnees_test = {"age" : 25, "sex" : "male", "bmi" : 24.5, "children" : 2, "smoker" : "yes", "region" : "southwest"}
    pred = prediction(chemin_modele, donnees_test)
    assert pred is not None
    assert isinstance(pred, float)



