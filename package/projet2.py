import csv
import requests
from bs4 import BeautifulSoup

def write_csv(csv_files_dir, category_name, book_items_dict, books_dicts_list):
    fieldnames = book_items_dict.values()
    with open(f"{csv_files_dir}/{category_name}.csv", "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()
        for book_dict in books_dicts_list:
            writer.writerow(book_dict)

def get_book_information(category_name, book_items_dict, root_url, book_url):
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
        image_url = str(product_gallery.img["src"]).replace("../../", f"{root_url}")
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
