import pandas as pd
import numpy as np
from assets.model_prediction import *
from assets.data_preparation_functions import *

import tkinter as tk
from tkinter import filedialog
import tkinter as tk    
import  pickle


# Initialiser Tkinter
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale

#1. Recuperation des colonnes du fichier csv
file_path = filedialog.askopenfilename()
colonnes=pd.read_csv(file_path).columns
colonnes=colonnes.tolist()




#["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S"]
liste_colonnes_csv=[]
liste_colonnes_modele = ['conn_state', 'duration', 'ts','local_orig', 'local_resp', 'protocol',
       'service', 'history', 'src_ip', 'src_port', 'orig_bytes', 'orig_pkts',
       'orig_ip_bytes', 'dest_ip', 'dest_port', 'resp_bytes', 'resp_pkts',
       'resp_ip_bytes', 'missed_bytes', "ID Unique de la connexion ('None' si pas présent)"]

#2. Demande du nom des colonnes
for i in liste_colonnes_modele:
    nom=""
    erreur=True
    while erreur:
        erreur=False
        nom=str(input("Entrez le nom de la colonne correspondant à '"+i+"' : "))
        if nom!="None":
            if nom=="":
                erreur=True
                print("Nom de colonne vide")
            if nom not in colonnes:
                erreur=True
                print("Nom de colonne incorrect")
            elif nom in liste_colonnes_csv:
                erreur=True
                print("Nom de colonne déjà utilisé")
    liste_colonnes_csv.append(nom)


#3. Ouverture du fichier et transformation des données
data=open_clean_transform_data(file_path,liste_colonnes_csv)
print(data.head())
print(data.shape)
print(data.columns)

#4. appel de la fonction de prédiction

data_predict=load_model_and_predict(model_path="Distribution/assets/lightgbm_model_package.pkl",data=data)
print(data_predict)
print(data_predict.columns)

root.deiconify()  # Make sure the root window is visible
root.update()
output_path = filedialog.asksaveasfilename(defaultextension=".csv")
data_predict.to_csv(output_path, index=False)
root.withdraw()



