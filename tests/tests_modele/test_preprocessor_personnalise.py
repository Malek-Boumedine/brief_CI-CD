import os
import sys
import pytest
p_path = os.getcwd()
sys.path.append(p_path)
from src.main import Preprocessor_Personnalise

import pandas as pd
from src.main import Preprocessor_Personnalise, categorie_bmi, categorie_age



@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "age": [25, 30, 45, 60, 18],
        "sex": ["male", "female", "male", "female", "male"],
        "bmi": [18.0, 24.9, 25.0, 34.9, 40.0],
        "smoker": ["yes", "non", "non", "yes", "non"],
        "region": ["north", "south", "east", "west", "north"],
        "children": [0, 1, 2, 3, 4]
    })

@pytest.fixture
def preprocessor():
    return Preprocessor_Personnalise()

class Test_Preprocessor_Personnalise:
    def test_initialization(self, preprocessor):
        assert hasattr(preprocessor, "encodeur_smoker")
        assert hasattr(preprocessor, "encodeur_sex")
        assert hasattr(preprocessor, "encodeur_region")

    def test_fit(self, preprocessor, sample_data):
        preprocessor.fit(sample_data)
        assert preprocessor.region_columns is not None
        assert preprocessor.bmi_cat_columns is not None
        assert preprocessor.age_cat_columns is not None

    def test_transform_structure(self, preprocessor, sample_data):
        preprocessor.fit(sample_data)
        transformed = preprocessor.transform(sample_data)
        # Vérifie qu'il n'y a plus les colonnes catégorielles originales
        assert "region" not in transformed.columns
        assert "bmi_cat" not in transformed.columns
        assert "age_cat" not in transformed.columns

    def test_transform_values(self, preprocessor, sample_data):
        preprocessor.fit(sample_data)
        transformed = preprocessor.transform(sample_data)
        # Vérifie les encodages binaires
        assert set(transformed["smoker"].unique()).issubset({0, 1})
        assert set(transformed["sex_male"].unique()).issubset({0, 1})

    def test_handle_unknown_category(self, sample_data):
        # Ajoute une nouvelle région non vue dans le fit
        train = sample_data.copy()
        test = sample_data.copy()
        test.loc[0, "region"] = "unknown_region"
        preprocessor = Preprocessor_Personnalise()
        preprocessor.fit(train)
        transformed = preprocessor.transform(test)
        # Vérifie que la transformation ne plante pas et que toutes les colonnes sont présentes
        assert all(col in transformed.columns for col in preprocessor.region_columns)



