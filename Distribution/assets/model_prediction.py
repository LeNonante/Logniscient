import pickle
import lightgbm as lgb
import pandas as pd


def load_model_and_predict(model_path: str,data: pd.DataFrame):
    """Charge un modèle, encode les données catégorielles et effectue les predictions
    
    Args:
        model_path (str): Le chemin du fichier à ouvrir
        data (pd.DataFrame): Le dataframe à prédire

    Returns:
        pd.DataFrame: Le dataframe nettoyé et transformé
    """
    # Charger le fichier pickle
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)

    # Récupérer les éléments sauvegardés
    gbm = model_package['model']
    encoders = model_package['encoders']
    features = model_package['features']

    #Encodage des données catégorielles
    #Injection des données dqns le modele (sans la colonne 'ID' si présente)
    #Recuperation des predictions
    #Coller les colonnes ID et predictions
    #Renvoyer le DF 