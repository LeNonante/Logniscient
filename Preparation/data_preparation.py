import pandas as pd
import numpy as np
import os


# Load data
def load_data(data_path):
    return pd.read_csv(data_path)

#clean data
def clean_data(df):
    df["duration"] = df["duration"].fillna(0) #On remplace les durees vides par 0
    df["orig_bytes"] = df["orig_bytes"].fillna(0) #On remplace les orig_bytes vides par 0
    df["resp_bytes"] = df["resp_bytes"].fillna(0) #On remplace les resp_bytes vides par 0
    df["ts"] = pd.to_datetime(df["ts"], unit="s")
    df["date"] = df["ts"].dt.date   # recupere la date de la colonne ts
    df["heure"] = df["ts"].dt.time  # recupere l'heure de la colonne ts
    df = df.drop('datetime', axis=1) # on supprime la colonne datetime
    
    df = df.drop('uid', axis=1) # on supprime la colonne uid
    df = df.drop('community_id', axis=1) # on supprime la colonne community_id
    df = df.drop('ts', axis=1) # on supprime la colonne community_id
    
    return df

#save data
def save_data(df, data_path):
    df.to_csv(data_path, index=False)
    
#Get all csv files in a directory and its subdirectories    
def get_csv_files(data_dir):
    csv_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".csv"):
                sub_dir = os.path.basename(root)
                csv_files.append((sub_dir, file))
    return csv_files

# Recuperer les fichiers csv
data_dir = 'data/brut/UWF_TestZeekData24'
csv_files = get_csv_files(data_dir)
print(csv_files)

#les charger, les nettoyer et les sauvegarder
for i in csv_files:
    sub_dir = i[0]
    file = i[1]
    data_path = data_dir+"/"+sub_dir+"/"+file
    df = load_data(data_path)
    df = clean_data(df)
    data_path = "data/clean/"+sub_dir+".csv"
    save_data(df, data_path)
    