import cv2
import pyzbar.pyzbar as pyzbar

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

class User:
    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.is_admin = admin

def scan_qr_code():
    video_capture = cv2.VideoCapture(0)

    while True:
        _, frame = video_capture.read()

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            book_id = obj.data.decode('utf-8')
            return book_id

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def home_page():
    print("==== Library Management System ====")
    print("1. Login")
    print("2. Exit")

def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user.username == username and user.password == password:
            print("Login successful!")
            return user

    print("Login failed!")
    return None

def logout(user):
    print("Logout successful!")
    return 0

def book_management(library, user):
    while True:
        print("\n==== Book Management ====")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Find Book by ID")
        print("4. Scan QR Code")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            if user.is_admin == "admin":
                book_id = input("Enter Book ID: ")
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                book = Book(book_id, title, author)
                library.add_book(book)
                print("Book added successfully!")
            else:
                print("Only admins can add books!")

        elif choice == '2':
            if user.is_admin == "admin":
                book_id = input("Enter Book ID: ")
                book = library.find_book_by_id(book_id)
                if book:
                    library.remove_book(book)
                    print("Book removed successfully!")
                else:
                    print("Book not found!")
            else:
                print("Only admins can remove books!")

        elif choice == '3':
            book_id = input("Enter Book ID: ")
            book = library.find_book_by_id(book_id)
            if book:
                print("Title:", book.title)
                print("Author:", book.author)
            else:
                print("Book not found!")

        elif choice == '4':
            book_id = scan_qr_code()
            book = library.find_book_by_id(book_id)
            if book:
                print("Title:", book.title)
                print("Author:", book.author)
            else:
                print("Book not found!")

        elif choice == '5':
            logout(user)
            break

library = Library()
admin_user = User("admin", "password", "admin")
book_management(library,admin_user)
