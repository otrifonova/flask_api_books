# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models import User, Book, Edition, Author, Role, Publisher, Language, EditionAuthor
from app.api.responses import error_response


@bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    # валидация полученных данных
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in data:
            return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    if User.query.filter_by(username=data["username"]).first():
        return error_response(409, "Please use a different username")

    if User.query.filter_by(email=data["email"]).first():
        return error_response(409, "Please use a different email")
    # добавление нового пользователя
    new_user = User(username=data["username"],
                    email=data["email"])

    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    response = jsonify({"message": f"{new_user} was created"})
    response.status_code = 201
    return response


@bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json() or {}
    # валидация полученных данных
    required_fields = ["username", "password"]
    for field in required_fields:
        if field not in data:
            return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return error_response(401, f"User {data['username']} doesn't exist")
    elif not user.check_password(data["password"]):
        return error_response(401, f"Wrong password")
    else:  # создание JWT-токена
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return jsonify({
            "message": f"Logged in as {user.username}",
            "access_token": access_token,
            "refresh_token": refresh_token
        })


@bp.route("/token/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh_token():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    return jsonify({'access_token': access_token})


@bp.route("/editions/<int:id>", methods=["GET"])
@jwt_required()
def get_edition(id):
    edition = Edition.query.get(id)
    if edition:
        return jsonify(edition.to_dict())
    else:
        return error_response(404, f"Edition with id = {id} doesn't exist")


@bp.route("/editions", methods=["GET"])
def get_all_editions_by_book_id():
    book_id = request.args.get("book_id")
    if book_id:
        editions = Edition.query.filter_by(book_id=book_id).all()
        if editions:
            data = {"editions": [edition.to_dict(limited=True) for edition in editions]}
            return jsonify(data)
        else:
            return error_response(404, f"Book with id = {book_id} doesn't exist")


@bp.route("/editions", methods=["POST"])
def create_edition():
    data = request.get_json() or {}

    # валидация полученных данных
    required_fields = ["title", "publisher", "language", "authors", "isbn", "year", "text"]
    for field in required_fields:
        if field not in data:
            return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    required_fields_in_authors = ["name", "role", "order"]
    for item in data["authors"]:
        for field in required_fields_in_authors:
            if field not in item:
                return error_response(400, f"Authors must include fields: {', '.join(required_fields_in_authors)}")

    edition = Edition.query.filter_by(isbn=data["isbn"]).first()
    if edition:
        response = error_response(400, f"Edition with ISBN {edition.isbn} already exists (id = {edition.id})")
        response.headers["Location"] = url_for("get_edition", id=edition.id)
        return response

    # берем данные из таблиц Book, Publisher, Language, если нет - создаем
    title = data["title"]
    book = Book.query.filter_by(title=title).first()
    if not book:
        book = Book(title=title)
        db.session.add(book)
        db.session.commit()
    data["book_id"] = book.id

    publisher_name = data["publisher"]
    publisher = Publisher.query.filter_by(name=publisher_name).first()
    if not publisher:
        publisher = Publisher(name=publisher_name)
        db.session.add(publisher)
        db.session.commit()
    data["publisher_id"] = publisher.id

    language_name = data["language"]
    language = Language.query.filter_by(name=language_name).first()
    if not language:
        language = Language(name=language_name)
        db.session.add(language)
        db.session.commit()
    data["language_id"] = language.id

    # создаем запись о редакции в таблице Edition
    edition = Edition()
    edition.from_dict(data)
    db.session.add(edition)
    db.session.commit()

    # разбираем авторов, для каждого создаем запись в EditionAuthor
    authors = data["authors"]
    for author_item in authors:
        author_name = author_item["name"]
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)

        role_name = author_item["role"].lower()
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)

        order = author_item["order"]
        db.session.commit()

        edition_author = EditionAuthor(edition_id=edition.id,
                                       author_id=author.id,
                                       role_id=role.id,
                                       order=order)
        db.session.add(edition_author)
        db.session.commit()

    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for('get_edition', id=edition.id)
    return response


@bp.route("/editions/<int:id>", methods=["PUT"])
def update_edition(id):
    edition = Edition.query.get(id)
    if not edition:
        return error_response(404, f"Edition with id = {id} doesn't exist")
    data = request.get_json() or {}

    # берем данные из таблиц Book, Publisher, Language, если нет - создаем
    title = data.get("title")
    if title:
        book = Book.query.filter_by(title=title).first()
        if not book:
            book = Book(title=title)
            db.session.add(book)
        data["book_id"] = book.id

    publisher_name = data.get("publisher")
    if publisher_name:
        publisher = Publisher.query.filter_by(name=publisher_name).first()
        if not publisher:
            publisher = Publisher(name=publisher_name)
            db.session.add(publisher)
        data["publisher_id"] = publisher.id

    language_name = data.get("language")
    if language_name:
        language = Language.query.filter_by(name=language_name).first()
        if not language:
            language = Language(name=language_name)
            db.session.add(language)
        data["language_id"] = language.id

    # редактируем в таблице Edition
    edition.from_dict(data)
    db.session.commit()

    response = jsonify({})
    response.status_code = 204
    return response


@bp.route("/editions/<int:id>", methods=["DELETE"])
def delete_edition(id):
    edition = Edition.query.filter_by(id=id)
    if not edition.first():
        return error_response(404, f"Edition with id = {id} doesn't exist")
    EditionAuthor.query.filter_by(edition_id=id).delete()
    edition.delete()
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response
