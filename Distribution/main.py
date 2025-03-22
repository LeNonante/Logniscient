import pandas as pd
import numpy as np
from assets.model_prediction import *
from assets.data_preparation_functions import *

import tkinter as tk
from tkinter import filedialog
import tkinter as tk    
import  pickle
import customtkinter as ctk
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image

def bouton_valider(): 
    #1. Recuperation des colonnes du fichier csv
    file_path = chemin_csv
    if file_path != "":
        liste_colonnes_csv=[]
        for combobox in column_comboboxes:
            liste_colonnes_csv.append(combobox.get())
        #3. Ouverture du fichier et transformation des données
        data=open_clean_transform_data(file_path,liste_colonnes_csv)
        print(data.head())
        print(data.shape)
        print(data.columns)

        #4. appel de la fonction de prédiction
        data_predict=load_model_and_predict(model_path="Distribution/assets/lightgbm_model_package.pkl",data=data)
        print(data_predict)
        print(data_predict.columns)

        #5. Sauvegarde du fichier
        output_path = filedialog.asksaveasfilename(defaultextension=".csv")
        data_predict.to_csv(output_path, index=False)
        

# Liste pour stocker les ComboBox
column_comboboxes = []
chemin_csv = ""
def choisir_csv():
    fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
    global chemin_csv
    chemin_csv = fichier
    if fichier:
        csv_entry.delete(0, "end")
        csv_entry.insert(0, fichier)
        # Charger les colonnes du CSV
        try:
            df = pd.read_csv(fichier, nrows=1)  # Lire seulement la première ligne pour récupérer les colonnes
            colonnes = df.columns.tolist()
            colonnes.append("None")  # Ajouter l'option "None" pour les colonnes non utilisées
            # Mettre à jour les listes déroulantes
            for i in range(len(column_comboboxes)):
                combobox = column_comboboxes[i]
                combobox.configure(values=colonnes)
                if colonnes :  
                    liste_combobox=liste_colonnes_modele
                    if liste_combobox[i] in colonnes:
                        combobox.set(liste_combobox[i])  # Sélectionner le meme nom si il est present
                    else:
                        combobox.set("Sélectionner une colonne")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
    

# Configurer CustomTkinter
ctk.set_appearance_mode("dark")  # Mode sombre
ctk.set_default_color_theme("dark-blue")
            
# Créer la fenêtre principale
root = ctk.CTk()
root.title("Logniscient")
root.geometry("735x655")
root.resizable(False, False)

# Conteneur principal
frame = ctk.CTkFrame(root, fg_color="#262424")  # Fond noir
frame.pack(expand=True, fill="both", padx=20, pady=20)
# Définition des couleurs
BG_COLOR = "#262424"  # Fond sombre
TEXT_COLOR = "#5A6063"  # Texte beige clair
ENTRY_BG = "#343638"  # Fond des champs d'entrée

# Titre
# Charger l'image avec transparence
ratio_image = 1/4.7
img = ctk.CTkImage(light_image=Image.open("Distribution/assets/LogoLogniscient.png"), size=(689*ratio_image, 474*ratio_image))
#title_label = ctk.CTkLabel(frame, text="Logniscient", font=("Arial", 24, "bold"), text_color="white")
title_label = ctk.CTkLabel(frame, image=img, text="")
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Champ CSV
csv_label = ctk.CTkLabel(frame, text="CSV", font=("Arial", 14), text_color="white")
csv_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

csv_entry = ctk.CTkEntry(frame, width=400)
csv_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky="w")

csv_button = ctk.CTkButton(frame, text="Parcourir", width=80, command=choisir_csv)
csv_button.grid(row=1, column=3, padx=10, pady=5)

liste_colonnes_modele = ['conn_state', 'duration', 'ts','local_orig', 'local_resp', 'protocol',
       'service', 'history', 'src_port', 'orig_bytes', 'orig_pkts',
       'orig_ip_bytes', 'dest_port', 'resp_bytes', 'resp_pkts',
       'resp_ip_bytes', 'missed_bytes', "ID Unique de la connexion\n('None' si pas présent)"]

for i in range(9):  # 9 colonnes à gauche
    label = ctk.CTkLabel(frame, text=liste_colonnes_modele[i], font=("Arial", 12), text_color="white")
    label.grid(row=i+2, column=0, padx=10, pady=5, sticky="e")
    
    combobox = ctk.CTkComboBox(frame, width=200, fg_color=ENTRY_BG, button_color=TEXT_COLOR, button_hover_color="#CCCCCC", state="readonly")
    combobox.grid(row=i+2, column=1, pady=5, sticky="w")
    combobox.set("Sélectionner une colonne")
    column_comboboxes.append(combobox)
    
for i in range(9):  # 9 colonnes à droite
    label = ctk.CTkLabel(frame, text=liste_colonnes_modele[i+9], font=("Arial", 12), text_color="white")
    label.grid(row=i+2, column=2, padx=10, pady=5, sticky="e")

    combobox = ctk.CTkComboBox(frame, width=200, fg_color=ENTRY_BG, button_color=TEXT_COLOR, button_hover_color="#CCCCCC", state="readonly")
    combobox.grid(row=i+2, column=3, pady=5, sticky="w")
    combobox.set("Sélectionner une colonne")
    column_comboboxes.append(combobox)

# Ajouter un bouton à la place de l'Entry en bas
submit_button = ctk.CTkButton(
    frame, 
    command=bouton_valider, 
    text="Valider",  
    fg_color="#007BFF",  # Bleu
    hover_color="#0056b3",  # Bleu plus foncé au survol
    text_color="white",
    font=("Arial", 14, "bold"),
    width=150,  # Réduit la largeur
    height=40   # Optionnel : ajuste la hauteur si nécessaire
)
# Centrer le bouton en utilisant 'columnspan' et 'sticky'
submit_button.grid(row=15, column=0, columnspan=10, pady=25)
# Lancer l'application
root.mainloop()








