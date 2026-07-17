from colorsys import yiq_to_rgb
from fileinput import close
import json

with open('data.json', 'r') as f:
    data = json.load(f)

user_choice = 0
list_of_resurses = {}
list_of_readers = {}

class LibraryItem:
     def __init__(self, number, title, author, p_year, stock):
         self.title = title
         self.author = author
         self.p_year = p_year
         self.stock = stock
         self.number = number

     def book_info(self):
        return f"{self.title} от {self.author}, публикувана {self.p_year}"

class Book(LibraryItem):
    def __init__(self, number, title, author, p_year, stock, ISBN, pages):
        super().__init__(number, title, author, p_year, stock)
        self.ISBN = ISBN
        self.pages = pages
class EBook(LibraryItem):
    def __init__(self, number, title, author, p_year, f_format, f_size, stock):
        super().__init__(number, title, author, p_year, stock)
        self.f_format = f_format
        self.f_size = f_size

class Reader:
     def __init__(self, name, number, rent_books=None):
         self.name = name
         self.number = number
         self.rent_books = rent_books if rent_books is not None else []


#Управляващ клас
class Library:
    def __init__(self):
        self.list_of_resurses = []
        self.list_of_readers = []
        self.running = True
        self.load_data()
    def run_app(self):
        while self.running:
            self.show_menu()
            try:
                user_choice = int(input("Въведете цифрата за желаното от Вас действие: "))
            except ValueError as e:
                print()
                print()
                print()
                print(f"Възникна грешка: {e}/Моля въведете цифра.")
            if user_choice == 1:
                self.add_book()
            if user_choice == 2:
                self.add_ebook()
            if user_choice == 3:
                print(len(self.list_of_resurses))
            #Времевата сложност на линейното търсене е O(n)
            if user_choice == 4:
                self.linear_search_for_title()
            if user_choice == 5:
                self.sort_title()
            if user_choice == 6:
                self.sort_year()
            if user_choice == 7:
                self.register_reader()
            if user_choice == 8:
                self.list_readers()
            if user_choice == 9:
                self.borrow_book()
            if user_choice == 10:
                self.return_book()
            if user_choice == 11:
                self.show_taken()
            if user_choice == 12:
                self.save_data()
                print("Изход от програмата...")
                self.running = False

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)

            self.list_of_resurses = []
            for d in data.get("resurses_json", []):
                if "f_format" in d:
                    self.list_of_resurses.append(EBook(**d))
                else:
                    self.list_of_resurses.append(Book(**d))

            self.list_of_readers = [Reader(**d) for d in data.get("readers_json", [])]
        except (FileNotFoundError, json.JSONDecodeError):
            self.list_of_resurses = []
            self.list_of_readers = []
    def show_menu(self):
                print("===НАЧАЛНО МЕНЮ===")
                print("1. Добавяне на книга")
                print("2. Добавяне на Екнига")
                print("3. Виж всички книги")
                print("4. Регистриране на читатели")
                print("5. Читатели")
                print("6. Търсене на заглавие")
                print("7. Сортиране на книги по заглавие")
                print("8. Сортиране на книги по година")
                print("9. Вземане на книги")
                print("10. Връщане на книги")
                print("11. Излез")
    def save_data(self):
        data = {
            "resurses_json": [r.__dict__ for r in self.list_of_resurses],
            "readers_json": [r.__dict__ for r in self.list_of_readers]
        }
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
    def __len__(self):
        return len(self.list_of_resurses)
    def return_book(self):
        returner = input()
        returned_book = input()
        for resurse in self.list_of_resurses:
            if returned_book == resurse.title:
                for reader in self.list_of_readers:
                    if returner == reader.name:
                        if len(reader.rent_books) != 0:
                            for rented in reader.rent_books:
                                if returned_book == rented:
                                    reader.rent_books.remove(rented)
                                    resurse.stock +=1
                                    print(f"{returner} върна {returned_book}")
                                else:
                                    print(f"{returner} не е взимал {returned_book}")
                        else:
                            print(f"{returner} няма взети книги!")
                    else:
                        continue
                        print(f"Няма такова име в системата ни")
            else:
                continue
                print(f"{returned_book} не е в библиотеката ни.")
    def add_book(self):
        book = Book(input("Въведи уникален номер: "), input("Въведи заглавие: "), input("Въведи автор: "),
                    int(input("Въведи дата на издаване: ")), int(input("Въведи бройки: ")), input("Въведи ISBN код: "),
                    input("Въведи брой страници: "))
        self.list_of_resurses.append(book)
        self.save_data()
        print(f"{book.title} беше успешно добавена!")
    def add_ebook(self):
        ebook = EBook(input("Въведи уникален номер: "), input("Въведи заглавие: "), input("Въведи автор: "),
                      int(input("Въведи дата на издаване: ")),
                      input("Въведи файлов формат: "), input("Въведи размер на файла: "),
                      int(input("Въведи брой лицензи: ")))
        self.list_of_resurses.append(ebook)
        self.save_data()
        print(f"{ebook.title} беше успешно добавена!")
    def register_reader(self):
        reader = Reader(input("Въведете име на читателя: "), input("Въведете номер на читателя: "))
        self.list_of_readers.append(reader)
        self.save_data()
        print("Читателят беше успешно добавен")
        user_choice = 0
    def list_readers(self):
        for reader in self.list_of_readers:
            print(reader.name, reader.number)
    def search_by_title(self):
        search = input()
        for resurse in self.list_of_resurses:
            if search != resurse.title:
                continue
            else:
                print(f"{resurse.title} е налична.")
    def borrow_book(self):
        borrower = input()
        borrowed = input()
        for resurse in self.list_of_resurses:
            if borrowed == resurse.title:
                if resurse.stock > 0:
                    for reader in self.list_of_readers:
                        if borrower == reader.name:
                            if len(reader.rent_books) == 0:
                                    reader.rent_books.append(resurse.title)
                                    resurse.stock -=1
                                    self.save_data()
                                    print(f"{borrower} взе {borrowed}")
                            else:
                                double_check = any(borrowed == rented for rented in reader.rent_books)
                                if double_check == True:
                                    print(f"{borrower} вече е взел {borrowed}")
                                else:
                                    for rented in reader.rent_books:
                                        if len(reader.rent_books) < 3:
                                            reader.rent_books.append(resurse.title)
                                            resurse.stock -= 1
                                            self.save_data()
                                            print(f"{borrower} взе {borrowed}")
                                        else:
                                            print(f"{borrower} е взел 3 книги")
                        else:
                            continue
                            print("Въведете истинско име на читател")
                else:
                    print("Няма налично копие")
            else:
                continue
                print("Въведете име на книга от ресурсите ни!")
    def sort_title(self):
        by_title = sorted(self.list_of_resurses, key=lambda resurse: resurse.title)
        for resurse in by_title:
            print(resurse)
    def sort_year(self):
        by_year = sorted(self.list_of_resurses, key=lambda resurse: resurse.p_year)
        for resurse in by_year:
            print(resurse)
    def show_taken(self):
        for reader in self.list_of_readers:
            if len(reader.rent_books) > 0:
                print(f"{reader.name} е заел {reader.rent_books}")
            else:
                continue

