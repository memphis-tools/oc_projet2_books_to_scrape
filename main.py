import os
import time
from package import projet2

#déclarations modifiables
csv_files_dir = "csv_files"
root_url = "https://books.toscrape.com"

#déclarations à ne pas modifier
product_information_dict = {}
books_dicts_list = []

#Définition d'un dictionnaire pour les libellés, en-tetes des fichiers .csv
#Les informations à récupérer se présentent comme :
#des champs individuels hors ul. On préformatte clef et valeur : "category", "title" ...
#des lignes d'une "ul". Içi la clef sera l'intitulé réel, et en valeur celui qu'on choisit
#Enfin les intitulés en valeurs servent aussi pour l'écriture des en-tetes des .csv
book_items_dict = {
    "category": "category",
    "title": "title",
    "product_page_url": "product_page_url",
    "image_url": "image_url",
    "UPC": "universal_product_code",
    "Price (incl. tax)": "price_including_tax",
    "Price (excl. tax)": "price_excluding_tax",
    "product_description": "product_description",
    "Product Type": "product_type",
    "Tax": "tax",
    "Availability": "number_available",
    "Number of reviews": "review_rating",
}

if csv_files_dir not in os.listdir():
    os.mkdir(csv_files_dir)

#phase 1
#category_name par défaut pour test de la phase 1
category_name = "Mystery"
#book_uri et book_url par défaut pour test de la phase 1
book_uri = "catalogue/the-murder-of-roger-ackroyd-hercule-poirot-4_852/index.html"
book_url = f"{root_url}/{book_uri}"
print("[DEBUG PHASE 1] Exemple avec 'The Murder of Roger Ackroyd' de la catégorie 'Mystery'")
books_dicts_list.append(projet2.get_book_information(category_name, book_items_dict, root_url, book_url))
projet2.write_csv(csv_files_dir, category_name, book_items_dict, books_dicts_list)
