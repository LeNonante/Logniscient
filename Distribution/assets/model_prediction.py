import pickle
import lightgbm as lgb
import pandas as pd
import numpy as np

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

    print(encoders)
    # Convertir en tableau NumPy pour accélérer les modifications
    # Récupérer toutes les colonnes sauf 'label tactique'
    columns_to_modify = [col for col in encoders.keys() if col != 'label_tactic']

    # Extraire les colonnes à modifier
    data_array = data[columns_to_modify].values
    num_rows, num_cols = data_array.shape
    
    for i in range(num_rows):
        # Modifier directement les valeurs
        for col in columns_to_modify:
             for j, col in enumerate(encoders.keys()):  # `j` est l'index correspondant dans `data_array`
                if col != 'label_tactic':
                    if data_array[i, j] not in encoders[col].classes_:  
                        data_array[i, j] = "unknown"
            

    # Remettre les données modifiées dans le DataFrame
    data[columns_to_modify] = data_array
    
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
    tableau_predictions = gbm.predict(X_new)
    print(tableau_predictions)
    #Sélectionner la classe avec la plus haute probabilité
    predictions = tableau_predictions.argmax(axis=1)

    #Sélectionner la probabilité de malveillance (première colonne du tableau numpy)
    probas = tableau_predictions[:,:1]
    probas=np.round(probas,4)#On arrondit les probabilités à 4 chiffres après la virgule 

    probas_df = pd.DataFrame(probas, columns=['Probabilité de malveillance'])

    # Reconvertir en labels textuels pour l'évaluation
    predictions_class = encoders['label_tactic'].inverse_transform(predictions)
    #reconvertir les labels de data
    for col in ['conn_state', 'protocol', 'service', 'history']:
        data[col] = encoders[col].inverse_transform(data[col])
    #Ajouter les prédictions au dataset
    data['Prediction'] = predictions_class
    data['Probabilité de malveillance'] = probas

    #Renvoyer le DataFrame avec les prédictions
    if id_present:
        data['ID']=df_id
        data=data[['ID','conn_state', 'duration', 'local_orig', 'local_resp', 'protocol',
            'service', 'history', 'src_ip', 'src_port', 'orig_bytes', 'orig_pkts',
            'orig_ip_bytes', 'dest_ip', 'dest_port', 'resp_bytes', 'resp_pkts',
            'resp_ip_bytes', 'missed_bytes', 'Prediction','Probabilité de malveillance']]
    return data
