import pickle
import lightgbm as lgb
import pandas as pd

def load_model_and_predict(model_path: str, data: pd.DataFrame):
    """
    Charge un modèle, encode les données catégorielles et effectue les prédictions
    
    Args:
        model_path (str): Le chemin du fichier contenant le modèle sauvegardé
        data (pd.DataFrame): Le dataframe à prédire

    Returns:
        pd.DataFrame: Le dataframe avec les prédictions
    """
    # Charger le fichier pickle
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)

    # Récupérer les éléments sauvegardés
    gbm = model_package['model']  # Modèle entraîné
    encoders = model_package['encoders']  # Encodeurs pour les variables catégorielles
    features = model_package['features']  # Liste des features utilisées pour l'entraînement


    #Sauvegarder la colonne ID et surpprimer ID si elle est présente
    id_present=False
    if 'ID' in data.columns:
        df_id=data['ID']
        data.drop(columns=['ID'],inplace=True)
        id_present=True

    #Encodage des données catégorielles si nécessaire
    for col, encoder in encoders.items():
        if col in data.columns:
            data[col] = encoder.transform(data[col].astype(str))
    
    # Sélection des bonnes colonnes pour la prédiction
    X_new = data[features]
    
    #Effectuer les prédictions
    predictions = gbm.predict(X_new)
    print(predictions)
    #Sélectionner la classe avec la plus haute probabilité
    predictions = predictions.argmax(axis=1)
    # Reconvertir en labels textuels pour l'évaluation
    predictions_class = encoders['label_tactic'].inverse_transform(predictions)
    #reconvertir les labels de data
    for col in ['conn_state', 'protocol', 'service', 'history']:
        data[col] = encoders[col].inverse_transform(data[col])
    #Ajouter les prédictions au dataset
    data['Prediction'] = predictions_class
    
    #Renvoyer le DataFrame avec les prédictions
    if id_present:
        data['ID']=df_id
        data=data[['ID','conn_state', 'duration', 'local_orig', 'local_resp', 'protocol',
            'service', 'history', 'src_ip', 'src_port', 'orig_bytes', 'orig_pkts',
            'orig_ip_bytes', 'dest_ip', 'dest_port', 'resp_bytes', 'resp_pkts',
            'resp_ip_bytes', 'missed_bytes', 'Prediction']]
    return data



