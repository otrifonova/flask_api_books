from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def attr_exists(cls, attr_name, attr_value):
        col = cls.__table__.columns.get(attr_name)
        return bool(cls.query.filter(col == attr_value).first())

    @classmethod
    def get_required_fields(cls):
        required_fields = cls.__table__.columns.keys()
        if "id" in required_fields:
            required_fields.remove("id")
        return required_fields

    @classmethod
    def get_columns(cls):
        columns = []
        for col in cls.__dict__.keys():
            if not col.startswith("_"):
                columns.append(col)
        return columns

    def to_dict_inner(self):
        columns = self.__table__.columns.keys()
        data = {}
        for col in columns:
            data[col] = self.__getattribute__(f"{col}")
        return data

    def to_dict(self):
        columns = self.get_columns()
        data = {}
        for col in columns:
            value = self.__getattribute__(f"{col}")
            if value and not isinstance(value, (int, str)):
                if isinstance(value, BaseModel):
                    data[col] = value.to_dict_inner()
                else:
                    if len(value) <= 1:
                        for v in value:
                            data[col] = v.to_dict_inner()
                    else:
                        data[col] = []
                        for v in value:
                            data[col].append(v.to_dict_inner())
            else:
                data[col] = value
        return data

    def from_dict(self, data):
        columns = self.__table__.columns
        for col in columns:
            if col.name in data:
                self.__setattr__(col.name, data[col.name])


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

    def exists(self):
        if User.query.filter((User.username == self.username) | (User.email == self.email)).first():
            return True
        else:
            return False


class EditionAuthor(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    edition_id = db.Column(db.Integer, db.ForeignKey("edition.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    order = db.Column(db.Integer)
    author = db.relationship("Author", viewonly=True)
    role = db.relationship("Role", viewonly=True)
    # book = db.relationship("Book",
    #                         secondary="join(Edition, Book, Edition.book_id==Book.id)",
    #                         primaryjoin="(EditionAuthor.edition_id == Edition.id)",
    #                         backref="edition_author")


class Book(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    editions = db.relationship("Edition", cascade="all, delete-orphan")
    # authors = db.relationship("Author",
    #                           secondary="join(EditionAuthor, Edition, EditionAuthor.edition_id==Edition.id)",
    #                           primaryjoin="(Edition.book_id == Book.id)")


class Author(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    # books = db.relationship("Book",
    #                         secondary="join(EditionAuthor, Edition, EditionAuthor.edition_id==Edition.id)",
    #                         primaryjoin="(EditionAuthor.author_id == Author.id)")


class Role(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Publisher(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)


class Language(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Edition(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", viewonly=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"))
    publisher = db.relationship("Publisher", viewonly=True)
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    language = db.relationship("Language", viewonly=True)
    year = db.Column(db.Integer)
    text = db.Column(db.Text)
    edition_author = db.relationship("EditionAuthor", cascade="all, delete-orphan")
    # authors = db.relationship("Author",
    #                           secondary="join(EditionAuthor, Author, EditionAuthor.author_id==Author.id)",
    #                           primaryjoin=(EditionAuthor.edition_id == id))


class ModelGetter:
    _models = {"author": Author,
               "book": Book,
               "edition": Edition,
               "edition_author": EditionAuthor,
               "language": Language,
               "publisher": Publisher,
               "role": Role,
               }

    _foreign_keys = {"author_id": Author,
                     "book_id": Book,
                     "edition_id": Edition,
                     "edition_author_id": EditionAuthor,
                     "language_id": Language,
                     "publisher_id": Publisher,
                     "role_id": Role,
                     }

    @classmethod
    def get_model(cls, m):
        return cls._models[m]

    @classmethod
    def get_foreign_keys(cls, m):
        foreign_keys = set(cls._models[m].get_required_fields()) & set(cls._foreign_keys.keys())
        foreign_keys_dict = {}
        for fk in foreign_keys:
            foreign_keys_dict[fk] = cls._foreign_keys[fk]
        return foreign_keys_dict
