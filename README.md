<p align="center">
  <img src="Logo/LogoLogniscient.png" alt="Logniscient 🔎" width="400">
</p>

# Logniscient 🔎

Logniscient est une intelligence artificielle développée par [Groulor](https://github.com/Groulor), [LeNonante](https://github.com/LeNonante) et [Orty](https://github.com/orty-orty) pour assister l'équipe de l'association Hack'UTT dans l'analyse de fichiers de logs pour la [European Cyber Cup](https://european-cybercup.com/). Son objectif est d'identifier rapidement et efficacement les signes de menaces potentielles en automatisant la détection d'anomalies et d'activités suspectes.

## Fonctionnalités 🚀
- Détection des comportements malveillants à partir de logs

## Technologies utilisées 🛠️
- **Langage** : Python
- **Machine Learning** : LightGBM
- **Traitement des logs** : Pandas
- **Visualisation** : Matplotlib / Seaborn

## Installation 📂
### Prérequis
Assurez-vous d'avoir Python installé (>= 3.8). Vous pouvez vérifier votre version avec :
```sh
python --version
```

### Installation des dépendances
Cloner le projet et installer les dépendances nécessaires :
```sh
git clone https://github.com/LeNonante/Logniscient.git
cd Logniscient
pip install -r requirements.txt
```

## Utilisation 📖
1. **Lancer le script principal** :
   ```sh
   python main.py
   ```
2. **Sélectionner un fichier CSV** contenant les logs à analyser.
3. **Remplir les champs** en associant les colonnes du CSV aux catégories requises par le modèle.
   - Un fois le CSV chargé, les colonnes ayant le même nom que celles attendues seront automatiquement détéctées
   - Pour les colonnes ayant un nom différent, sélectionnez le nom correspondant dans votre CSV via la liste déroulante
4. **Valider et choisir un fichier de sortie** pour sauvegarder les résultats de l'analyse.

## Licence 📜
Ce projet est sous licence MIT.

## Auteurs 🖋️
- [Groulor](https://github.com/Groulor)
- [LeNonante](https://github.com/LeNonante)
- [Orty](https://github.com/orty-orty)
