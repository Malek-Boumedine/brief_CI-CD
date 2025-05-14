from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder, StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error
from sklearn.linear_model import Lasso
import pandas as pd
import numpy as np
import joblib
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir))

# fonction pour importer les données
def charger_donnees(fichier = "src/dataset_assurance.csv") :
    try : 
        data = pd.read_csv(fichier)
        data = data.drop_duplicates()
        return data
    except FileNotFoundError as e :
        raise e
    except pd.errors.ParserError as e: 
        raise e
    

def creer_exporter_modele(chemin_modele) : 
    
    data = charger_donnees()
    if data is not None and isinstance(data, pd.DataFrame) and not data.empty:
        X = data.drop("charges", axis=1)
        y = data["charges"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size=0.85, random_state=42, stratify=X["smoker"])

        model = creer_pipeline()
        model.fit(X_train, y_train)
        joblib.dump(model, chemin_modele)
        return "modele exporté avec succès"
    

def charger_modele(chemin_modele) : 
    return joblib.load(chemin_modele)
    

def prediction(chemin_modele, data:dict) : 
    modele = charger_modele(chemin_modele)
    df1 = pd.DataFrame([data])
    return round(modele.predict(df1)[0], 2)


# fonction pour afficher les metriques
def metriques(model, X_test, y_test) :
    
    if X_test is None or y_test is None or len(X_test) == 0 or len(y_test) == 0:
        raise ValueError("X_test ou y_test est vide")
    
    pred_y = model.predict(X_test)
    mse = mean_squared_error(y_test, pred_y)
    mae = mean_absolute_error(y_test, pred_y)
    r2 = r2_score(y_test, pred_y)
    med_ae = median_absolute_error(y_test, pred_y)

    print(f"MSE : {mse}")
    print(f"RMSE : {np.sqrt(mse)}")
    print(f"MAE : {mae}")
    print(f"R2 : {r2}")
    print(f"MedAE : {med_ae}")

    return mse, mae, r2, med_ae


# fonction pour transformer les catégories d"age
def categorie_age(age) :

    if not isinstance(age, (int, float)):
        raise TypeError("L'âge doit être un nombre.")
    if age < 0:
        raise ValueError("L'âge ne peut pas être négatif.")
    if age > 110 : 
        raise ValueError("Age trop élevé, vérifiez votre saisie")
    if age < 25:
        return "24 et moins"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 55:
        return "45-54"
    else:
        return "55 et plus"


# fonction pour transformer les catégories de bmi
def categorie_bmi(bmi):
    
    if not isinstance(bmi, (int, float)):
        raise TypeError("Le BMI doit être un nombre.")
    if bmi < 0:
        raise ValueError("Le BMI ne peut pas être négatif.")
    if bmi > 100:
        raise ValueError("BMI trop élevé, vérifiez votre saisie.")
    if bmi < 18.5:
        return "insuffisance pondérale"
    elif bmi < 24.5:
        return "normal"
    elif bmi < 30:
        return "surpoids"
    elif bmi < 35:
        return "obésité I"
    elif bmi < 40:
        return "obésité II"
    else:
        return "obésité III"


# preprocesseur personnalisé
class Preprocessor_Personnalise(BaseEstimator, TransformerMixin):

    def __init__(self):

        self.encodeur_smoker = LabelBinarizer(pos_label=1, neg_label=0)
        self.encodeur_sex = LabelBinarizer(pos_label=1, neg_label=0)
        self.encodeur_region = OneHotEncoder(sparse_output=False, handle_unknown='ignore') # Ajout de handle_unknown
        self.encodeur_bmi_cat = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore') # Ajout pour bmi_cat
        self.encodeur_age_cat = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore') # Ajout pour age_cat

        # classes des encodeurs
        self.encodeur_smoker.classes_ = ["yes", "non"]
        self.encodeur_sex.classes_ = np.array(["male", "female"])

        self.region_columns = None
        self.bmi_cat_columns = None
        self.age_cat_columns = None

    def fit(self, X, y=None):

        # encodage des X cats
        self.encodeur_smoker.fit(X["smoker"])
        self.encodeur_sex.fit(X["sex"])
        self.encodeur_region.fit(X[["region"]])
        self.region_columns = self.encodeur_region.get_feature_names_out(["region"])

        # Création des catégories avant le fit des encodeurs one-hot
        X_copie = X.copy()
        X_copie["bmi_cat"] = X_copie["bmi"].apply(categorie_bmi)
        X_copie["age_cat"] = X_copie["age"].apply(categorie_age)

        self.encodeur_bmi_cat.fit(X_copie[["bmi_cat"]])
        self.bmi_cat_columns = self.encodeur_bmi_cat.get_feature_names_out(["bmi_cat"])

        self.encodeur_age_cat.fit(X_copie[["age_cat"]])
        self.age_cat_columns = self.encodeur_age_cat.get_feature_names_out(["age_cat"])

        return self

    def transform(self, X):

        X_copie = X.copy()

        # encodage smoker et sex
        X_copie["smoker"] = self.encodeur_smoker.transform(X_copie["smoker"])
        X_copie["sex"] = self.encodeur_sex.transform(X_copie["sex"])
        X_copie.rename(columns={"sex": "sex_male"}, inplace=True)

        # encodage region
        region_encodee = self.encodeur_region.transform(X_copie[["region"]])
        df_region_encodee = pd.DataFrame(
            region_encodee,
            columns=self.region_columns,
            index=X_copie.index
        )

        # concat et drop
        X_copie = pd.concat([X_copie, df_region_encodee], axis=1)
        X_copie.drop("region", axis=1, inplace=True)

        # création categories bmi et age
        X_copie["bmi_cat"] = X_copie["bmi"].apply(categorie_bmi)
        X_copie["age_cat"] = X_copie["age"].apply(categorie_age) # Correction ici

        # onehot encodage bmi_cat
        bmi_cat_encodee = self.encodeur_bmi_cat.transform(X_copie[["bmi_cat"]])
        df_bmi_cat_encodee = pd.DataFrame(
            bmi_cat_encodee,
            columns=self.bmi_cat_columns,
            index=X_copie.index
        )
        X_copie = pd.concat([X_copie, df_bmi_cat_encodee], axis=1)
        X_copie.drop("bmi_cat", axis=1, inplace=True)

        # onehot encodage age_cat
        age_cat_encodee = self.encodeur_age_cat.transform(X_copie[["age_cat"]])
        df_age_cat_encodee = pd.DataFrame(
            age_cat_encodee,
            columns=self.age_cat_columns,
            index=X_copie.index
        )
        X_copie = pd.concat([X_copie, df_age_cat_encodee], axis=1)
        X_copie.drop("age_cat", axis=1, inplace=True)

        return X_copie


# pipeline
def creer_pipeline() : 
    pipeline = Pipeline([
        ("preprocessor", Preprocessor_Personnalise()),
        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
        ("scaler", StandardScaler()),
        ("feature_selection", SelectKBest(score_func=f_regression, k=50)),
        ("regressor", Lasso(alpha=238, random_state=42))
    ])
    return pipeline


def main():
    pass

##################################################################

if __name__ == "__main__" :
    
    # chargement des données
    data = charger_donnees()
    
    if data and isinstance(data, pd.DataFrame) :
        X = data.drop("charges", axis=1)
        y = data["charges"]

        # split trainset testset
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size=0.85, random_state=42, stratify=X["smoker"])

        pipeline = creer_pipeline()
    
        # entrainement
        pipeline.fit(X_train, y_train)

        # evaluation
        metriques(model=pipeline, X_test=X_test, y_test=y_test)
        
        # sauvegarde pipeline
        creer_exporter_modele(pipeline, "complete_pipeline")

        # test sur nos données
        valeurs1 = {"age" : 34, "sex" : "male", "bmi" : 24.5, "children" : 0, "smoker" : "no", "region" : "southwest"}
        print("#"*25)
        df1 = pd.DataFrame([valeurs1])
        print("Prime prédite :", round(pipeline.predict(df1)[0], 2))
    else : 
        print("Erreur chargement des données :", data)









