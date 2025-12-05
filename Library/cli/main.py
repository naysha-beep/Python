#Task4
# cli/main.py

import logging

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

def main():
    inventory = LibraryInventory()
    inventory.load_from_file()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            book = Book(title, author, isbn)
            inventory.add_book(book)
            inventory.save_to_file()
            print("Book added successfully.")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ").strip()
            books = inventory.search_by_isbn(isbn)
            if books and books[0].issue():
                inventory.save_to_file()
                print("Book issued.")
            else:
                print("Book not available.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ").strip()
            books = inventory.search_by_isbn(isbn)
            if books and books[0].return_book():
                inventory.save_to_file()
                print("Book returned.")
            else:
                print("Book not issued.")

        elif choice == "4":
            for b in inventory.display_all():
                print(b)

        elif choice == "5":
            title = input("Enter title: ").strip()
            results = inventory.search_by_title(title)
            if results:
                for b in results:
                    print(b)
            else:
                print("No book found.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
