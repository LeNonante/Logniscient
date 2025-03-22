import pandas as pd
import numpy as np
import ipaddress


def clean_data(df:pd.DataFrame):
    """Nettoie les données du dataframe en paramètre
    
    On remplace les valeurs manquantes par des valeurs par défaut, on supprime les colonnes inutiles

    Args:
        df (pd.DataFrame): Le dataframe à nettoyer

    Returns:
        pd.DataFrame: Le dataframe nettoyé
    """
    df["duration"] = df["duration"].fillna(0) #On remplace les durees vides par 0
    df["orig_bytes"] = df["orig_bytes"].fillna(0) #On remplace les orig_bytes vides par 0
    df["resp_bytes"] = df["resp_bytes"].fillna(0) #On remplace les resp_bytes vides par 0
    df["service"] = df["service"].fillna("unknow") #On remplace les service vides par unknow
    df["history"] = df["history"].fillna("unknow") #On remplace les history vides par 0

    #on supprime les colonnes inutiles
    colonnes_a_garder=["conn_state","duration","local_orig","local_resp","protocol","service","history","ts","src_port", "orig_bytes","orig_pkts","orig_ip_bytes","dest_port","resp_bytes","resp_pkts","resp_ip_bytes","missed_bytes","ID"]
    for c in df.columns:
        if c not in colonnes_a_garder:
            df.drop(c, axis=1, inplace=True)

    return df

def transform_data(df:pd.DataFrame):
    """Transforme les données du dataframe en paramètre
    
    On convertit les données en format adapté pour le modèle
    
    Args:
        df (pd.DataFrame): Le dataframe à transformer"""

    df['ts'] = pd.to_datetime(df['ts'], unit='s') #on décompose la colonne ts en plusieurs colonnes

    df = df.sort_values('ts')
    df['time_since_last'] = df['ts'].diff().dt.total_seconds()

    # Remplacer la première valeur NaN par 0 ou une autre valeur appropriée
    df['time_since_last'] = df['time_since_last'].fillna(0)

    df=df.drop(['ts'], axis=1)#On supprime la colonne ts

    return df


def open_clean_transform_data(CSV_file:str, liste_colonnes_csv:list): 
    """Renvoie un dataframe pandas nettoyé et transformé du fichier CSV en paramètre

    Les colonnes sont renommées pour etre traitées par le modèle.
    
    Args:
        CSV_file (str): Chemin vers le fichier CSV à ouvrir
        liste_colonnes_csv (list[str]): Liste du nom des colonnes du fichier CSV (pour les renommer correctement)

    Returns:
        pd.DataFrame: Le dataframe nettoyé et transformé
    """
    liste_colonnes_modele = ['conn_state', 'duration', 'ts','local_orig', 'local_resp', 'protocol',
       'service', 'history', 'src_port', 'orig_bytes', 'orig_pkts',
       'orig_ip_bytes', 'dest_port', 'resp_bytes', 'resp_pkts',
       'resp_ip_bytes', 'missed_bytes']
    
    # Load data
    data = pd.read_csv(CSV_file)
    #Rennomer les colonnes
    for i in range(len(liste_colonnes_modele)):
        ancien_nom = liste_colonnes_csv[i]
        nouveau_nom = liste_colonnes_modele[i]
        data=data.rename(columns={ancien_nom: nouveau_nom})

    #On renomme la derniere colonne en ID si elle existe
    if liste_colonnes_csv[-1].upper()!="NONE" :
        data=data.rename(columns={liste_colonnes_csv[-1]: "ID"})

    # Clean data
    data = clean_data(data)
    
    # Transform data
    data = transform_data(data)
    
    return data

