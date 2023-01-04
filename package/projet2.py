import csv
import os
import requests
import time
from bs4 import BeautifulSoup
from vars import vars

def create_default_folders(folders_to_create):
    for var_dir in folders_to_create:
        if var_dir not in os.listdir():
            os.mkdir(var_dir)

def write_csv(category_name, books_dicts_list):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    books_dicts_list: liste avec tous les livres sous forme de dictionnaire
    """
    fieldnames = vars.book_items_dict.values()

    with open(f"{vars.csv_files_dir}/{category_name}.csv", "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
        for book_dict in books_dicts_list:
            writer.writerow(book_dict)

def download_image(category_name, img_url):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    img_url: URL absolue de l'image
    """
    file_name = f"{img_url[img_url.rindex('/'):]}"
    if category_name not in os.listdir(vars.img_files_dir):
        os.mkdir(f"{vars.img_files_dir}/{category_name}")
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(f"{vars.img_files_dir}/{category_name}{file_name}", 'wb') as img_file:
            img_file.write(response.content)

def get_book_information(category_name, book_url):
    """
    Paramètres:
    category_name: une String (exemple: 'Travel')
    book_url: URL complète d'un livre (exemple: 'https://...island-2_277/index.html')
    """
    product_information_dict = {}
    response = requests.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_information_dict["category"] = category_name
        title = soup.find("li", {"class": "active"}).text
        product_information_dict["title"] = title
        star_rating = soup.find("div", {"class", "product_main"}).findAll("p")[2]
        product_information_dict["star_rating"] = star_rating['class'][1]
        product_information_dict["product_page_url"] = book_url
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
        time.sleep(1)
    return product_information_dict

def get_category_books(category_name, category_uri, soup, category_books_uri_list = []):
    """
    Paramètres:
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
        response = requests.get(f"{vars.root_url}/{formated_uri}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            time.sleep(1)
        category_books_uri_list = get_category_books(category_name, category_uri, soup)

    return category_books_uri_list

def get_categories_uri_dict():
    response = requests.get(f"{vars.root_url}/index.html")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        categories_ul = soup.find("ul", {"class": "nav-list"}).find("ul").findAll("li")
        categories_uri_dict = {category.a.text.strip():category.a['href'] for category in categories_ul}

    return categories_uri_dict

def get_categories_books():
    categories_uri_dict = get_categories_uri_dict()
    total_books = 0
    for category_name, category_uri in categories_uri_dict.items():
        books_dicts_list = []
        response = requests.get(f"{vars.root_url}/{category_uri}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            category_books_uri_list = get_category_books(category_name, category_uri, soup)
            for book_uri in category_books_uri_list:
                books_dicts_list.append(get_book_information(
                    category_name,
                    f"{vars.root_url}/{book_uri}",
                ))
                total_books += 1

            write_csv(category_name, books_dicts_list)
            category_books_uri_list.clear()

    return total_books
