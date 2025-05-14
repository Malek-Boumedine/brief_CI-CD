import os
import sys
p_path = os.getcwd()
sys.path.append(p_path)
import pytest
from modele.main import categorie_bmi



def test_categorie_bmi():
    # cas normaux
    assert categorie_bmi(0) == "insuffisance pondérale"
    assert categorie_bmi(18.4) == "insuffisance pondérale"
    assert categorie_bmi(18.5) == "normal"
    assert categorie_bmi(24.4) == "normal"
    assert categorie_bmi(24.5) == "surpoids"
    assert categorie_bmi(29.9) == "surpoids"
    assert categorie_bmi(30) == "obésité I"
    assert categorie_bmi(34.9) == "obésité I"
    assert categorie_bmi(35) == "obésité II"
    assert categorie_bmi(39.9) == "obésité II"
    assert categorie_bmi(40) == "obésité III"
    assert categorie_bmi(60) == "obésité III"
    assert categorie_bmi(100) == "obésité III"

    # bmi négatif
    for bmi in [-1, -20]:
        with pytest.raises(ValueError, match="Le BMI ne peut pas être négatif."):
            categorie_bmi(bmi)

    # bmi > 100
    for bmi in [101, 150, 1000, float('inf')]:
        with pytest.raises(ValueError, match="BMI trop élevé, vérifiez votre saisie."):
            categorie_bmi(bmi)

    # type invalide
    for bmi in ["vingt", None, [], {}]:
        with pytest.raises(TypeError, match="Le BMI doit être un nombre."):
            categorie_bmi(bmi)
