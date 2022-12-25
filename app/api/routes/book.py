# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Book
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/book/<int:id>", methods=["GET"])
@jwt_required()
def get_book(id):
    book = Book.query.get(id)
    if book:
        return jsonify(book.to_dict())
    else:
        return error_response(404, f"Book with id = {id} doesn't exist")


@bp.route("/book", methods=["POST"])
@jwt_required()
def create_book():
    data = request.get_json() or {}

    required_fields = ("title",)
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    title = data["title"]
    book = Book(title=title)
    db.session.add(book)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_book', id=book.id)
    return response


@bp.route("/book/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return error_response(404, f"Book with id = {id} doesn't exist")

    data = request.get_json() or {}
    new_title = data.get("title")
    if not new_title:
        return error_response(400, 'Field "title" is empty')

    book.title = new_title
    db.session.commit()
    return success_response(204)


@bp.route("/book/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return error_response(404, f"Book with id = {id} doesn't exist")

    db.session.delete(book)
    db.session.commit()
    return success_response(204)
