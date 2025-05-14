import os
import sys
p_path = os.getcwd()
sys.path.append(p_path)
import pytest
from modele.main import categorie_age



def test_categorie_age():
    # cas normaux
    assert categorie_age(0) == "24 et moins"
    assert categorie_age(10) == "24 et moins"
    assert categorie_age(24) == "24 et moins"
    assert categorie_age(25) == "25-34"
    assert categorie_age(34) == "25-34"
    assert categorie_age(35) == "35-44"
    assert categorie_age(44) == "35-44"
    assert categorie_age(45) == "45-54"
    assert categorie_age(54) == "45-54"
    assert categorie_age(55) == "55 et plus"
    assert categorie_age(80) == "55 et plus"
    assert categorie_age(110) == "55 et plus"

    # age négatif
    for age in [-1, -100]:
        with pytest.raises(ValueError, match="L'âge ne peut pas être négatif."):
            categorie_age(age)

    # age > 110
    for age in [111, 150, 1_000_000, float('inf')]:
        with pytest.raises(ValueError, match="Age trop élevé, vérifiez votre saisie"):
            categorie_age(age)

    # type invalide
    for age in ["trente", None, [], {}]:
        with pytest.raises(TypeError, match="L'âge doit être un nombre."):
            categorie_age(age)




