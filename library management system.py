"""Library Management System (OOP)."""

from datetime import date, timedelta


class LibraryError(Exception):
    pass


class Book:
    def __init__(self, book_id, title, author, copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available = copies

    def __str__(self):
        return f"[{self.book_id}] {self.title} by {self.author} ({self.available}/{self.total_copies})"


class Patron:
    MAX_BOOKS = 3

    def __init__(self, patron_id, name):
        self.patron_id = patron_id
        self.name = name
        self.borrowed = []

    def __str__(self):
        return f"[{self.patron_id}] {self.name} - {len(self.borrowed)} borrowed"


class BorrowRecord:
    def __init__(self, book_id, patron_id):
        self.book_id = book_id
        self.patron_id = patron_id
        self.issue_date = date.today()
        self.due_date = self.issue_date + timedelta(days=14)
        self.return_date = None

    def __str__(self):
        status = "returned" if self.return_date else "issued"
        return f"{self.book_id} -> {self.patron_id} ({status}, due {self.due_date})"


class Library:
    def __init__(self):
        self.books = {}
        self.patrons = {}
        self.records = []

    def add_book(self, book_id, title, author, copies=1):
        if book_id in self.books:
            self.books[book_id].total_copies += copies
            self.books[book_id].available += copies
        else:
            self.books[book_id] = Book(book_id, title, author, copies)

    def register_patron(self, patron_id, name):
        if patron_id in self.patrons:
            raise LibraryError("Patron already registered.")
        self.patrons[patron_id] = Patron(patron_id, name)

    def issue_book(self, book_id, patron_id):
        book = self.books.get(book_id)
        patron = self.patrons.get(patron_id)
        if not book or not patron:
            raise LibraryError("Book or patron not found.")
        if book.available < 1:
            raise LibraryError(f"'{book.title}' is not available.")
        if len(patron.borrowed) >= Patron.MAX_BOOKS:
            raise LibraryError(f"{patron.name} has reached the borrow limit.")

        book.available -= 1
        patron.borrowed.append(book_id)
        record = BorrowRecord(book_id, patron_id)
        self.records.append(record)
        return record

    def return_book(self, book_id, patron_id):
        book = self.books.get(book_id)
        patron = self.patrons.get(patron_id)
        if not book or not patron or book_id not in patron.borrowed:
            raise LibraryError("This book was not issued to this patron.")

        record = next(r for r in self.records
                       if r.book_id == book_id and r.patron_id == patron_id and not r.return_date)
        record.return_date = date.today()
        book.available += 1
        patron.borrowed.remove(book_id)
        return record

    def available_books(self):
        return [b for b in self.books.values() if b.available > 0]


if __name__ == "__main__":
    lib = Library()
    lib.add_book("B1", "Clean Code", "Robert Martin", 2)
    lib.add_book("B2", "The Pragmatic Programmer", "Andy Hunt", 1)

    lib.register_patron("P1", "Asha Verma")

    print("Issuing B1 to P1:", lib.issue_book("B1", "P1"))
    print("Returning B1:", lib.return_book("B1", "P1"))

    print("\nAvailable books:")
    for b in lib.available_books():
        print(b)
