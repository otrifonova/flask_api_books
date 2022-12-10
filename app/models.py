from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class EditionAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edition_id = db.Column(db.Integer, db.ForeignKey("edition.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    order = db.Column(db.Integer)
    author = db.relationship("Author")
    role = db.relationship("Role")
    books = db.relationship("Book",
                            secondary="join(Edition, Book, Edition.book_id==Book.id)",
                            primaryjoin="(EditionAuthor.edition_id == Edition.id)",
                            lazy="dynamic")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)
    editions = db.relationship("Edition", lazy="dynamic")
    authors = db.relationship("Author",
                              secondary="join(EditionAuthor, Edition, EditionAuthor.edition_id==Edition.id)",
                              primaryjoin="(Edition.book_id == Book.id)", lazy="dynamic")


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    books = db.relationship("Book",
                            secondary="join(EditionAuthor, Edition, EditionAuthor.edition_id==Edition.id)",
                            primaryjoin="(EditionAuthor.author_id == Author.id)", lazy="dynamic")


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Edition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book")
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"))
    publisher = db.relationship("Publisher")
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    language = db.relationship("Language")
    year = db.Column(db.Integer)
    text = db.Column(db.Text)
    authors = db.relationship("Author",
                              secondary="join(EditionAuthor, Author, EditionAuthor.author_id==Author.id)",
                              primaryjoin=(EditionAuthor.edition_id == id), lazy="dynamic")

    def to_dict(self, limited=False):
        data = {
            "id": self.id,
            "isbn": self.isbn,
            "book_id": self.book_id,
            "book_title": self.book.title,
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher.name,
            "language_id": self.language_id,
            "language_name": self.language.name,
            "year": self.year,
            "authors": [],
        }
        if not limited:
            data["text"] = self.text
        """
        authors = [{"author_id": author.id,
                    "author_name": author.name,
                    "author_role": author.role
                    } for author in self.authors]
        
        data["authors"] = authors
        """
        return data

    def from_dict(self, data):
        for field in ['isbn', 'year', 'text', 'book_id', 'publisher_id', 'language_id']:
            if field in data:
                setattr(self, field, data[field])
