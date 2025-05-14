import pandas as pd
import pytest
import os
import sys
p_path = os.getcwd()
sys.path.append(p_path)
from modele.main import charger_donnees



def test_fichier_introuvable() :
    with pytest.raises(FileNotFoundError) : 
        charger_donnees("src/test.csv")

    
def test_chargement_donnees_ok() : 
    data = charger_donnees()
    assert data is not None
    assert isinstance(data, pd.DataFrame)




