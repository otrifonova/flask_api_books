# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Book, Edition, Publisher, Language, EditionAuthor
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data, is_object_in_db


@bp.route("/edition/<int:id>", methods=["GET"])
@jwt_required()
def get_edition(id):
    edition = Edition.query.get(id)
    if edition:
        return jsonify(edition.to_dict())
    else:
        return error_response(404, f"Edition with id = {id} doesn't exist")


@bp.route("/edition", methods=["GET"])
@jwt_required()
def get_all_editions_by_book_id():
    book_id = request.args.get("book_id")
    if book_id:
        editions = Edition.query.filter_by(book_id=book_id).all()
        if editions:
            data = {"editions": [edition.to_dict(limited=True) for edition in editions]}
            return jsonify(data)
        else:
            return error_response(404, f"Book with id = {book_id} doesn't exist")


@bp.route("/edition", methods=["POST"])
@jwt_required()
def create_edition():
    data = request.get_json() or {}

    required_fields = ("isbn", "book_id", "publisher_id", "language_id", "year", "text")
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    response_message = []
    book_id = data.get("book_id")
    publisher_id = data.get("publisher_id")
    language_id = data.get("language_id")

    models = ((Book, book_id), (Publisher, publisher_id), (Language, language_id))
    for model, id in models:
        if id and not is_object_in_db(model, id):
            response_message.append(f"{model.get_name()} with id = {id} doesn't exist")

    if response_message:
        return error_response(404, response_message)

    edition = Edition()
    edition.from_dict(data)

    if edition.attr_exists("isbn", edition.isbn):
        response = error_response(400, f"Edition with ISBN {edition.isbn} already exists (id = {edition.id})")
        response.headers["Location"] = url_for("api.get_edition", id=edition.id)
        return response

    db.session.add(edition)
    db.session.commit()
    response = success_response(201)
    response.headers["Location"] = url_for("api.get_edition", id=edition.id)
    return response


@bp.route("/edition/<int:id>", methods=["PUT"])
@jwt_required()
def update_edition(id):
    edition = Edition.query.get(id)
    if not edition:
        return error_response(404, f"Edition with id = {id} doesn't exist")

    data = request.get_json() or {}
    response_message = []

    # проверяем, чтобы не было пустых или несуществующих внешних ключей
    foreign_keys = ((Book, "book_id"), (Publisher, "publisher_id"), (Language, "language_id"))
    for model, fk in foreign_keys:
        if fk in data:
            fk_id = data[fk]
            if not fk_id:
                response_message.append(f'Field "{fk}" cannot be empty')
            elif not is_object_in_db(model, fk_id):
                response_message.append(f"{model.get_name()} with id = {fk_id} doesn't exist")

    if response_message:
        return error_response(404, response_message)

    # проверяем, уникален ли ISBN
    new_isbn = data.get("isbn")
    if new_isbn and new_isbn != edition.isbn:
        temp_edition = Edition(isbn=new_isbn)
        if temp_edition.isbn_exists():
            response = error_response(400, f"Edition with ISBN {edition.isbn} already exists (id = {edition.id})")
            response.headers["Location"] = url_for("api.get_edition", id=edition.id)
            return response

    edition.from_dict(data)
    db.session.commit()
    return success_response(204)


@bp.route("/edition/<int:id>", methods=["DELETE"])
def delete_edition(id):
    edition = Edition.query.get(id)
    if not edition:
        return error_response(404, f"Edition with id = {id} doesn't exist")
    EditionAuthor.query.filter_by(edition_id=id).delete()
    db.session.delete(edition)
    db.session.commit()
    return success_response(204)
