

#Task 1
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = str(isbn).strip()
        status = status.lower().strip()
        if status not in {"available", "issued"}:
            raise ValueError("Status must be 'available' or 'issued'")
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def issue(self):
        """Mark the book as issued if available."""
        if self.status == "issued":
            return False   # already issued
        self.status = "issued"
        return True

    def return_book(self):
        """Mark the book as available if issued."""
        if self.status == "available":
            return False   # already available
        self.status = "available"
        return True

    def is_available(self):
        """Check if the book is currently available."""
        return self.status == "available"


#Task2


# library_manager/inventory.py
from .book import Book

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





