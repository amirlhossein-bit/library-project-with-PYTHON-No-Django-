import json

class Book:
    def __init__(self, title, author, book_id, available=True):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.available = available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "book_id": self.book_id,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        return Book(data["title"], data["author"], data["book_id"], data["available"])


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def to_dict(self):
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @staticmethod
    def from_dict(data):
        member = Member(data["name"], data["member_id"])
        member.borrowed_books = data["borrowed_books"]
        return member


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title, author, book_id):
        self.books.append(Book(title, author, book_id))
        print("📚 ketab ezafe shud.")

    def show_books(self):
        if not self.books:
            print("hich ketabi mojod nist.")
            return
        for book in self.books:
            status = "✅ mojod" if book.available else "❌ amant dade shod"
            print(f"{book.book_id} - {book.title} | {book.author} | {status}")

    def search_by_author(self, author):
        found = [book for book in self.books if author.lower() in book.author.lower()]
        if not found:
            print("ketabi ba in nevisande yaft nashud.")
        else:
            for book in found:
                print(f"{book.book_id} - {book.title} | {book.author}")

    def add_member(self, name, member_id):
        self.members.append(Member(name, member_id))
        print("👤 ozv jadid sabt shod.")

    def borrow_book(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not member:
            print("ozv piyda nashod.")
            return
        if not book:
            print("ketab piyda nashood.")
            return
        if not book.available:
            print("in ketab ghabla amant dade shode ast.")
            return

        book.available = False
        member.borrowed_books.append(book.book_id)
        print(f"📖 «{book.title}» be «{member.name}» amanat dade shod.")

    def return_book(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not member or not book:
            print("ovz ya ketab piyda nashod.")
            return

        if book_id not in member.borrowed_books:
            print("in ketab tavasot in ozv amanat nagerfte ast .")
            return

        book.available = True
        member.borrowed_books.remove(book.book_id)
        print(f"🔙 «{book.title}» tavasot «{member.name}»bazgardande shood.")

    def save_data(self, filename="library_data.json"):
        data = {
            "books": [b.to_dict() for b in self.books],
            "members": [m.to_dict() for m in self.members]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("💾 etelaat zakhire shod.")

    def load_data(self, filename="library_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(b) for b in data["books"]]
                self.members = [Member.from_dict(m) for m in data["members"]]
            print("📂 etelaat barguzari shood.")
        except FileNotFoundError:
            print("⚠️ file dade yaft nashod entekhab ba shoro khali..")


if __name__ == "__main__":
    lib = Library()
    lib.load_data()

    while True:
        print("\n---menu ketabkhane ---")
        print("1. afzodan ketab jadid")
        print("2. namayesh list ketab ha")
        print("3. jostejo ketab bar asas nevisande")
        print("4. sabt name ozv jadid")
        print("5. amanat gerftan ketab")
        print("6. pas dadn ketab")
        print("7. zakhire va khoroj")

        choice = input("entekhab shuma: ")
        if choice == "1":
            title = input("name ketab: ")
            author = input("name nevisande: ")
            book_id = input("code ketab: ")
            lib.add_book(title, author, book_id)

        elif choice == "2":
            lib.show_books()

        elif choice == "3":
            author = input("name nevisande: ")
            lib.search_by_author(author)

        elif choice == "4":
            name = input("name ozzv: ")
            member_id = input("code ozviat: ")
            lib.add_member(name, member_id)

        elif choice == "5":
            member_id = input("kod ozviat: ")
            book_id = input("code ketab: ")
            lib.borrow_book(member_id, book_id)

        elif choice == "6":
            member_id = input("code ozviat: ")
            book_id = input("code ketab: ")
            lib.return_book(member_id, book_id)

        elif choice == "7":
            lib.save_data()
            print("👋 khoroj az barname......")
            break

        else:
            print("❌ entekhab na motabar!")



