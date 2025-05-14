import os
import sys
import pytest
import numpy as np
p_path = os.getcwd()
sys.path.append(p_path)
from modele.main import charger_donnees, charger_modele, metriques
from sklearn.model_selection import train_test_split



def test_metriques_sur_vraies_donnees():
    data = charger_donnees()
    X = data.drop("charges", axis=1)
    y = data["charges"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size=0.85, random_state=42, stratify=X["smoker"])

    chemin_modele = "src/modele_test.pkl"
    modele = charger_modele(chemin_modele)

    mse, mae, r2, med_ae = metriques(modele, X_test, y_test)
    mse2, mae2, r2_2, med_ae2 = metriques(modele, X_test, y_test)
    
    assert isinstance(mse, float)
    assert isinstance(mae, float)
    assert isinstance(r2, float)
    assert isinstance(med_ae, float)
    assert mse >= 0
    assert mae >= 0
    assert -1 <= r2 <= 1
    assert r2 >= 0.7, "Le R² est trop faible (attendu >= 0.7)"
    assert mse == mse2, "MSE non reproductible"
    assert mae == mae2, "MAE non reproductible"    
        

def test_metriques_entrees_invalides():
    data = charger_donnees()
    X = data.drop("charges", axis=1)
    y = data["charges"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size=0.85, random_state=42, stratify=X["smoker"])

    chemin_modele = "src/modele_test.pkl"
    modele = charger_modele(chemin_modele)

    # Test avec y_test vide
    with pytest.raises(ValueError):
        metriques(modele, X_test, np.array([]))
    
    # Test avec X_test vide
    with pytest.raises(ValueError):
        metriques(modele, np.empty((0, X_test.shape[1])), y_test)
    
    # Test avec X_test et y_test de tailles différentes
    with pytest.raises(ValueError):
        metriques(modele, X_test[:-1], y_test)
    
    # Test avec modèle None
    with pytest.raises(AttributeError):
        metriques(None, X_test, y_test)
