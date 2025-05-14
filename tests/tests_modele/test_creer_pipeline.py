import os
import sys
import pytest
p_path = os.getcwd()
sys.path.append(p_path)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import Lasso
from modele.main import creer_pipeline, Preprocessor_Personnalise



def test_creer_pipeline():
    # Création du pipeline
    pipe = creer_pipeline()
    
    # Vérifications de base
    assert isinstance(pipe, Pipeline), "L'objet retourné n'est pas un Pipeline"
    assert len(pipe.steps) == 5, "Le pipeline devrait contenir 5 étapes"
    
    # Vérification des noms et types des étapes
    etapes_attendues = [
        ("preprocessor", Preprocessor_Personnalise),
        ("poly", PolynomialFeatures),
        ("scaler", StandardScaler),
        ("feature_selection", SelectKBest),
        ("regressor", Lasso)
    ]
    
    for (nom_etape, step_class), (actual_name, actual_obj) in zip(etapes_attendues, pipe.steps):
        # Vérification du nom de l'étape
        assert nom_etape == actual_name, f"Nom d'étape incorrect pour {step_class.__name__}"
        
        # Vérification du type de l'objet
        assert isinstance(actual_obj, step_class), (
            f"{actual_name} devrait être un {step_class.__name__}, "
            f"reçu {type(actual_obj).__name__}"
        )
    
    # Vérification des paramètres spécifiques
    # PolynomialFeatures
    poly = pipe.named_steps["poly"]
    assert poly.degree == 2, "degree devrait etre 2 pour l'etape PolynomialFeatures"
    assert not poly.include_bias, "include_bias devrait etre False"
    
    # SelectKBest
    selector = pipe.named_steps["feature_selection"]
    assert selector.score_func == f_regression, "Mauvais score_func pour SelectKBest"
    assert selector.k == 50, "k devrait être 50 pour SelectKBest"
    
    # Lasso
    lasso = pipe.named_steps["regressor"]
    assert lasso.alpha == 238, f"Alpha devrait être 238, reçu {lasso.alpha}"
    assert lasso.random_state == 42, f"random_state devrait être 42, reçu {lasso.random_state}"



