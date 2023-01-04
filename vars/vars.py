#déclarations modifiables
csv_files_dir = "csv_files"
img_files_dir = "img_files"
folders_to_create = [csv_files_dir, img_files_dir]
root_url = "https://books.toscrape.com"

#déclarations à ne pas modifier
category_books_uri_list = []

#Définition d'un dictionnaire pour les libellés, en-tetes des fichiers .csv
#Les informations à récupérer se présentent comme :
#- des champs individuels hors ul. On préformatte clef et valeur : "category", "title" ...
#- des lignes d'une "ul". Içi la clef sera l'intitulé réel, et en valeur celui qu'on choisit
#A noter, enfin, que les intitulés en valeurs servent aussi pour l'écriture des en-tetes des .csv
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
