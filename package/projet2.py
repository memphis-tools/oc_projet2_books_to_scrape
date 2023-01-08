import concurrent.futures
import csv
import os
import requests
import threading
from bs4 import BeautifulSoup
from vars import vars

thread_local = threading.local()
category_label= ""
books_dicts_dict = {}
product_information_dict = {}

def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def create_default_folders(folders_to_create):
    for var_dir in folders_to_create:
        if var_dir not in os.listdir():
            os.mkdir(var_dir)

def write_csv(category_name, books_dicts_dict):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    books_dicts_dict: liste avec tous les livres sous forme de dictionnaire
    """
    fieldnames = vars.book_items_dict.values()
    with open(f"{vars.csv_files_dir}/{category_name}.csv", "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
        for book in books_dicts_dict[category_name]:
            writer.writerow(book)

def download_image(category_name, img_url):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    img_url: URL absolue de l'image
    """
    session = get_session()
    file_name = f"{img_url[img_url.rindex('/'):]}"
    if category_name not in os.listdir(vars.img_files_dir):
        os.mkdir(f"{vars.img_files_dir}/{category_name}")
    response = session.get(img_url)
    if response.status_code == 200:
        with open(f"{vars.img_files_dir}/{category_name}{file_name}", 'wb') as img_file:
            img_file.write(response.content)

def get_book_information(category_book_uri_key, category_book_uri_value):
    """
    Paramètre:
    category_book_uri_key: Nom catégorie de la série de livres (exemple: 'Travel')
    category_book_uri_value: l'URL absolue d'un livre (exemple: 'https://....html')
    """
    global books_dicts_dict
    category_name = category_book_uri_key
    book_url = category_book_uri_value

    session = get_session()
    for url in book_url:
        with session.get(f"{vars.root_url}/{url}") as response:
            product_information_dict = {}
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                product_information_dict["category"] = category_name
                title = soup.find("li", {"class": "active"}).text
                product_information_dict["title"] = title
                star_rating = soup.find("div", {"class", "product_main"}).findAll("p")[2]
                product_information_dict["star_rating"] = star_rating['class'][1]
                product_information_dict["product_page_url"] = f"{vars.root_url}/{url}"
                product_gallery = soup.find("div", {"id": "product_gallery"})
                image_url = str(product_gallery.img["src"]).replace("../..", f"{vars.root_url}")
                product_information_dict["image_url"] = image_url
                try:
                    product_description = soup.find("div", {"id": "product_description"}).findNext('p')
                    product_information_dict["product_description"] = product_description.text
                except:
                    product_information_dict["product_description"] = ""
                product_information_table = soup.find("table")
                for info in product_information_table.findAll("tr"):
                    product_information_dict[f"{vars.book_items_dict[str(info.th.text)]}"] = info.td.text

                download_image(category_name, image_url)
                books_dicts_dict[category_name].append(product_information_dict)

def get_category_books(category_name, category_uri, soup, category_books_uri_list = {}):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    category_uri: URL relative (exemple: catalogue/category/books/travel_2/index.html')
    soup: contenu de la page index d'une catégorie (la 1ère de chaque catégorie)
    category_books_uri_list: par défaut vide lors du 1er appel. Mais est précisée lors du parcours récursif.
    """
    if not category_name in category_books_uri_list:
        category_books_uri_list[category_name] = []
    for e in soup.find("ol").findAll("div", {"class": "image_container"}):
        formated_uri = str(e.a["href"]).replace("../../..", "catalogue")
        category_books_uri_list[category_name].append(formated_uri)

    next_button = soup.find("li", {"class", "next"})
    if next_button is not None:
        pager = next_button.a["href"]
        formated_uri = f"{category_uri[:category_uri.rindex('/')]}/{pager}"
        response = requests.get(f"{vars.root_url}/{formated_uri}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")

        category_books_uri_list = get_category_books(category_name, category_uri, soup)

    return category_books_uri_list

def get_categories_uri_dict():
    session = get_session()
    with session.get(f"{vars.root_url}/index.html") as response:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            categories_ul = soup.find("ul", {"class": "nav-list"}).find("ul").findAll("li")
            categories_uri_dict = {category.a.text.strip():category.a['href'] for category in categories_ul}

    return categories_uri_dict

def get_categories_books():
    global category_label
    global books_dicts_dict
    session = get_session()
    categories_uri_dict = get_categories_uri_dict()
    category_books_uri_list = {}
    total_books = 0

    for category_name, category_uri in categories_uri_dict.items():
        response = session.get(f"{vars.root_url}/{category_uri}")
        if response.status_code == 200:
            category_label = category_name
            soup = BeautifulSoup(response.text, "lxml")
            category_books_uri_list = get_category_books(category_name, category_uri, soup)
            if category_name not in books_dicts_dict:
                books_dicts_dict[category_name] = []

            with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
                executor.map(get_book_information, category_books_uri_list, category_books_uri_list.values())

            write_csv(category_name, books_dicts_dict)
            category_books_uri_list.clear()

    return total_books
