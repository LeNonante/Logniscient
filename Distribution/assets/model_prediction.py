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
    if 'ID' in data.columns:
        df_id=data['ID']
        data.drop(columns=['ID'],inplace=True)
    
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
    
    #Ajouter les prédictions au dataset
    data['Prediction'] = predictions_class
    
    #Renvoyer le DataFrame avec les prédictions
    data['ID']=df_id
    return data
