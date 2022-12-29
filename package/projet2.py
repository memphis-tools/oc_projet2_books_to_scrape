import csv
import requests
import time
from bs4 import BeautifulSoup

def write_csv(csv_files_dir, category_name, book_items_dict, books_dicts_list):
    """
    Paramètres:
    csv_files_dir: variable alias qui pointe le répertoire des fichiers .csv
    category_name: une String (exemple: 'Travel')
    book_items_dict: le dictionnaire des libellés et en-têtes .csv
    books_dicts_list: liste avec tous les livres sous forme de dictionnaire
    """
    fieldnames = book_items_dict.values()
    with open(f"{csv_files_dir}/{category_name}.csv", "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
        for book_dict in books_dicts_list:
            writer.writerow(book_dict)

def get_book_information(root_url, category_name, book_items_dict, book_url):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    book_items_dict: le dictionnaire des libellés et en-têtes .csv
    root_url: la partie racine de l'URL, partagée pour les requêtes
    book_url: URL complète d'un livre (exemple: 'https://...island-2_277/index.html')
    """
    product_information_dict = {}
    response = requests.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        product_information_dict["category"] = category_name
        title = soup.find("li", {"class": "active"}).text
        product_information_dict["title"] = title
        product_information_dict["product_page_url"] = book_url
        product_gallery = soup.find("div", {"id": "product_gallery"})
        image_url = str(product_gallery.img["src"]).replace("../..", f"{root_url}")
        product_information_dict["image_url"] = image_url

        try:
            product_description = soup.find("div", {"id": "product_description"}).findNext('p')
            product_information_dict["product_description"] = product_description.text
        except:
            product_information_dict["product_description"] = ""

        product_information_table = soup.find("table")
        for info in product_information_table.findAll("tr"):
            product_information_dict[f"{book_items_dict[str(info.th.text)]}"] = info.td.text

    return product_information_dict

def get_category_books(root_url, category_name, category_uri, soup, category_books_uri_list = []):
    """
    Paramètres:
    root_url: la partie racine de l'URL, partagée pour les requêtes
    category_name: une String (exemple: 'Travel')
    category_uri: URL relative (exemple: catalogue/category/books/travel_2/index.html')
    soup: contenu de la page index d'une catégorie (la 1ère de chaque catégorie)
    category_books_uri_list: par défaut vide lors du 1er appel. Mais est précisée lors du parcours récursif.
    """

    for e in soup.find("ol").findAll("div", {"class": "image_container"}):
        formated_uri = str(e.a["href"]).replace("../../..", "catalogue")
        category_books_uri_list.append(formated_uri)

    next_button = soup.find("li", {"class", "next"})
    if next_button is not None:
        pager = next_button.a["href"]
        formated_uri = f"{category_uri[:category_uri.rindex('/')]}/{pager}"
        response = requests.get(f"{root_url}/{formated_uri}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            time.sleep(1)
        category_books_uri_list = get_category_books(root_url, category_name, category_uri, soup)

    return category_books_uri_list

def get_categories_uri_dict(root_url, categories_uri_dict):
    """
    Paramètres:
    root_url: la partie racine de l'URL, partagée pour les requêtes
    categories_uri_dict: liste des URL relatives de chaque catégorie
    """
    response = requests.get(f"{root_url}/index.html")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        categories_ul = soup.find("ul", {"class": "nav-list"}).find("ul").findAll("li")
        categories_uri_dict = {category.a.text.strip():category.a['href'] for category in categories_ul}
        time.sleep(1)
    return categories_uri_dict

def get_categories_books(csv_files_dir, root_url, book_items_dict, categories_uri_dict):
    """
    Paramètres:
    csv_files_dir: variable alias qui pointe le répertoire des fichiers .csv
    root_url: la partie racine de l'URL, partagée pour les requêtes
    book_items_dict: le dictionnaire des libellés et en-têtes .csv
    categories_uri_dict: liste des URL relatives de chaque catégorie
    """
    total_books = 0
    for category_name, category_uri in categories_uri_dict.items():
        books_dicts_list = []
        response = requests.get(f"{root_url}/{category_uri}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            category_books_uri_list = get_category_books(root_url, category_name, category_uri, soup)
            for book_uri in category_books_uri_list:
                books_dicts_list.append(get_book_information(root_url, category_name, book_items_dict, f"{root_url}/{book_uri}"))
                total_books += 1
            category_name = category_name.replace(" ", "_").lower()
            write_csv(csv_files_dir, category_name, book_items_dict, books_dicts_list)
            category_books_uri_list.clear()
            time.sleep(1)
    return total_books
