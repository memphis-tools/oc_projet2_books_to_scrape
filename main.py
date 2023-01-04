import os

from package import projet2
from vars import vars

projet2.create_default_folders(vars.folders_to_create)
total_books = projet2.get_categories_books()
