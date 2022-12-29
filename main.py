import os
from package import projet2

#déclarations modifiables
csv_files_dir = "csv_files"
img_files_dir = "img_files"
root_url = "https://books.toscrape.com"

#déclarations à ne pas modifier
product_information_dict = {}
books_dicts_list = []
category_books_uri_list = []
categories_uri_dict = {}
category_books_list = []

#Définition d'un dictionnaire pour les libellés, en-tetes des fichiers .csv
#Les informations à récupérer se présentent comme :
#des champs individuels hors ul. On préformatte clef et valeur : "category", "title" ...
#des lignes d'une "ul". Içi la clef sera l'intitulé réel, et en valeur celui qu'on choisit
#Enfin les intitulés en valeurs servent aussi pour l'écriture des en-tetes des .csv
book_items_dict = {
    "category": "category",
    "title": "title",
    "star-rating": "star_rating",
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
if img_files_dir not in os.listdir():
    os.mkdir(img_files_dir)
categories_uri_dict = projet2.get_categories_uri_dict(root_url, categories_uri_dict)
total_books = projet2.get_categories_books(csv_files_dir, img_files_dir, root_url, book_items_dict, categories_uri_dict)
