# [OpenClassRoom](https://openclassrooms.com/) - Parcours développeur Python
![Screenshot](oc_parcours_dev_python.png)
## Projet 2 - Webscraping

### Description projet

- [x] **Phase 1** - Choisir n'importe quelle page Produit sur le site de [Books to Scrape](https://books.toscrape.com/).
      Écrire un script Python qui visite cette page et en extrait les informations.
- [x] **Phase 2** - Choisir n'importe quelle catégorie sur le site de Books to Scrape. Écrire un script Python qui :
* consulte la page de la catégorie choisie
* extrait l'URL de la page Produit de chaque livre appartenant à cette catégorie. 
* combiné avec le travail déjà effectué dans la phase 1 : extrait les données produit de tous les livres de la catégorie choisie, puis écrit les données dans un seul fichier CSV.
- [x] **Phase 3** - Ensuite, étendre le travail à l'écriture d'un script qui consulte le site de Books to Scrape.
* extraire toutes les catégories de livres disponibles
* extraire les informations produit de tous les livres appartenant à toutes les différentes catégories. 
* ecrire les données dans un fichier CSV distinct pour chaque catégorie de livres.
- [x] **Phase 4** - Prolonger le travail existant pour télécharger et enregistrer le fichier image de chaque page Produit consulté.
---
## Comment utiliser le projet ?
1. Clone the repository

      `git clone git@github.com:memphis-tools/oc_projet2_books_to_scrape.git`
      
      `cd oc_projet2_books_to_scrape`

2. Setup a virtualenv 

      `python -m venv env`

      `source env/bin/activate`

      `pip install -U pip`

      `pip install -r requirements.txt`

3. Run code

      `python main.py`
