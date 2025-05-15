import os 
import sys
from main import charger_donnees
from main import creer_exporter_modele


# d = charger_donnees("src/dataset_assurance_invalide.csv")



nom_modele = "modele_test"
modele = creer_exporter_modele("modele_test")
model_file = os.system(f"ls src/{nom_modele}.pkl")

print(model_file)
