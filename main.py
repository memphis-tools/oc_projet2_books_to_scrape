import os
import requests
import time
from bs4 import BeautifulSoup
from package import projet2

#déclarations modifiables
csv_files_dir = "csv_files"
root_url = "https://books.toscrape.com"

#déclarations à ne pas modifier
product_information_dict = {}
books_dicts_list = []
category_books_uri_list = []

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

#phase 2
#category_name et category_uri par défaut pour test de la phase 2
category_name = "Mystery"
category_uri = "catalogue/category/books/mystery_3/index.html"
print("[DEBUG PHASE 2] Exemple avec la catégorie 'Mystery'")
response = requests.get(f"{root_url}/{category_uri}")
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")
    category_books_uri_list = projet2.get_category_books(root_url, category_name, category_uri, soup)
    for book_uri in category_books_uri_list:
        books_dicts_list.append(projet2.get_book_information(root_url, category_name, book_items_dict, f"{root_url}/{book_uri}"))
    category_name = category_name.replace(" ", "_").lower()
    projet2.write_csv(csv_files_dir, category_name, book_items_dict, books_dicts_list)
