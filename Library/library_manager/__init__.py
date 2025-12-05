##class Book:
##    def _init_(self,title,author,isbn,status="Available"):
##        self.title=title
##        self.author=author
##        self.isbn=isbn
##        self.status=status
##    def display_info(self):
##        print("Book details are as follows")
##        print("Title:",self.title)
##        print("Author:",self.author)
##        print("ISBN:",self.isbn)
##        print("Status:",self.status)
##    def issue_book(self):
##        if self.status == "Issued":
##            print("Book is already issued")
##        else:
##            self.status="Issued"
##            print("Book has been issued successfully")
##    def return_book(self):
##         if self.status=="Available":
##            print("Book is already available in library")
##         else:
##            self.status="Available"
##            print("Book returned successfully")
##    def  save_to_file(self):
##        try:
##            with open("library.txt","a") as f :
##                f.write(f"{self.title},{self.author},{self.isbn},{self.status}\n")
##        except:
##            print("Error while saving to file")
##
##
##n="y"
##while n.lower()=="y":
##    print("\n-----LIBRARY MENU------")
##    print("1. Add a Book")
##    print("2. View All Books")
##    print("3.Issue a Book")
##    print("4. Return a Book")
##    
##    choice=int(input("Enter your choice : "))
##    books=[ ]
##
##    if choice == 1:
##            title=input("Enter book title:")
##            author= input("Enter author name:")
##            isbn=input("Enter ISBN number:")
##            book=Book(title,author,isbn)
##            books.append(book)
##            book.save_to_file()
##            print(len(books))
##    elif choice == 2:
##           if not books:
##                print("No books available.")
##           else:
##                for b in books:
##                    b.display_details()
##    elif choice == 3:
##            isbn = input("Enter ISBN to issue: ")
##            for b in books:
##                if b.isbn == isbn:
##                    b.issue_book()
##                    break
##            else:
##                print("Book not found.")
##
##    elif choice == 4:
##            isbn = input("Enter ISBN to return: ")
##            for b in books:
##                if b.isbn == isbn:
##                    b.return_book()
##                    break
##            else:
##                print("Book not found.")
##
##    elif choice == 5:
##            break
##
##    else:
##         print("Invalid choice.")
##    n=input("Do you want to continue or exist(Y/N)")
# library_manager/book.py


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

##
###Task2
##
##
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

##
###Task3
##    # library_manager/inventory.py (continuation)
##import json
##from pathlib import Path
##import logging
##
##CATALOG_FILE = Path("library_catalog.json")
##
##class LibraryInventory:
##    # ... previous methods ...
##
##    def save_to_file(self):
##        try:
##            with open(CATALOG_FILE, "w") as f:
##                json.dump([book.to_dict() for book in self.books], f, indent=4)
##            logging.info("Catalog saved successfully.")
##        except Exception as e:
##            logging.error(f"Error saving catalog: {e}")
##
##    def load_from_file(self):
##        try:
##            if not CATALOG_FILE.exists():
##                logging.warning("Catalog file not found. Starting fresh.")
##                return
##            with open(CATALOG_FILE, "r") as f:
##                data = json.load(f)
##                self.books = [Book.from_dict(d) for d in data]
##            logging.info("Catalog loaded successfully.")
##        except Exception as e:
##            logging.error(f"Error loading catalog: {e}")
##            self.books = []
##
###task4
### cli/main.py
##from library_manager.inventory import LibraryInventory
##from library_manager.book import Book
##
##def main():
##    inventory = LibraryInventory()
##    inventory.load_from_file()
##
##    while True:
##        print("\n--- Library Menu ---")
##        print("1. Add Book")
##        print("2. Issue Book")
##        print("3. Return Book")
##        print("4. View All Books")
##        print("5. Search Book")
##        print("6. Exit")
##
##        choice = input("Enter choice: ").strip()
##
##        if choice == "1":
##            title = input("Title: ").strip()
##            author = input("Author: ").strip()
##            isbn = input("ISBN: ").strip()
##            book = Book(title, author, isbn)
##            inventory.add_book(book)
##            inventory.save_to_file()
##            print("Book added successfully.")
##
##        elif choice == "2":
##            isbn = input("Enter ISBN to issue: ").strip()
##            books = inventory.search_by_isbn(isbn)
##            if books and books[0].issue():
##                inventory.save_to_file()
##                print("Book issued.")
##            else:
##                print("Book not available.")
##
##        elif choice == "3":
##            isbn = input("Enter ISBN to return: ").strip()
##            books = inventory.search_by_isbn(isbn)
##            if books and books[0].return_book():
##                inventory.save_to_file()
##                print("Book returned.")
##            else:
##                print("Book not issued.")
##
##        elif choice == "4":
##            for b in inventory.display_all():
##                print(b)
##
##        elif choice == "5":
##            title = input("Enter title: ").strip()
##            results = inventory.search_by_title(title)
##            if results:
##                for b in results:
##                    print(b)
##            else:
##                print("No book found.")
##
##        elif choice == "6":
##            print("Exiting...")
##            break
##
##        else:
##            print("Invalid choice. Try again.")
##
##if __name__ == "__main__":
##    main()
###Task 5
### cli/main.py (top of file)
##import logging
##
##logging.basicConfig(
##    filename="library.log",
##    level=logging.INFO,
##    format="%(asctime)s - %(levelname)s - %(message)s"
##)
##






















