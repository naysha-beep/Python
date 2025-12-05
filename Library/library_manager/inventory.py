#Task2


### library_manager/inventory.py
##from .book import Book
##
##class LibraryInventory:
##    def __init__(self):
##        self.books = []
##
##    def add_book(self, book: Book):
##        self.books.append(book)
##
##    def search_by_title(self, title):
##        return [book for book in self.books if book.title.lower() == title.lower()]
##
##    def search_by_isbn(self, isbn):
##        return [book for book in self.books if book.isbn == str(isbn)]
##
##    def display_all(self):
##        return [str(book) for book in self.books]
# library_manager/inventory.py
from .book import Book
import json
from pathlib import Path
import logging

CATALOG_FILE = Path("library_catalog.json")

class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def search_by_title(self, title):
        return [book for book in self.books if book.title.lower() == title.lower()]

    def search_by_isbn(self, isbn):
        return [book for book in self.books if book.isbn == str(isbn)]

    def display_all(self):
        return [str(book) for book in self.books]

    def save_to_file(self):
        try:
            with open(CATALOG_FILE, "w") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
            logging.info("Catalog saved successfully.")
        except Exception as e:
            logging.error(f"Error saving catalog: {e}")

    def load_from_file(self):
        try:
            if not CATALOG_FILE.exists():
                logging.warning("Catalog file not found. Starting fresh.")
                return
            with open(CATALOG_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(d) for d in data]
            logging.info("Catalog loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading catalog: {e}")
            self.books = []
