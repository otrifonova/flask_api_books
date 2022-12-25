# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import EditionAuthor, Edition, Author, Role
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data, is_object_in_db


@bp.route("/edition_author/<int:id>", methods=["GET"])
@jwt_required()
def get_edition_author(id):
    edition_author = EditionAuthor.query.get(id)
    if edition_author:
        return jsonify(edition_author.to_dict())
    else:
        return error_response(404, f"EditionAuthor with id = {id} doesn't exist")


@bp.route("/edition_author", methods=["POST"])
@jwt_required()
def create_edition_author():
    data = request.get_json() or {}

    required_fields = ("edition_id", "author_id", "role_id", "order")
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    response_message = []
    edition_id = data.get("edition_id")
    author_id = data.get("author_id")
    role_id = data.get("role_id")
    order = data.get("order")

    models = [(Edition, edition_id), (Author, author_id), (Role, role_id)]
    for model, id in models:
        if id and not is_object_in_db(model, id):
            response_message.append(f"{model.get_name()} with id = {id} doesn't exist")

    edition_author = EditionAuthor(edition_id=edition_id,
                                   author_id=author_id,
                                   role_id=role_id,
                                   order=order)
    db.session.add(edition_author)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_edition_author', id=edition_author.id)
    return response


@bp.route("/edition_author/<int:id>", methods=["PUT"])
@jwt_required()
def update_edition_author(id):
    edition_author = EditionAuthor.query.get(id)
    if not edition_author:
        return error_response(404, f"EditionAuthor with id = {id} doesn't exist")

    data = request.get_json() or {}
    response_message = []

    # проверяем, чтобы не было пустых или несуществующих внешних ключей
    foreign_keys = ((Edition, "edition_id"), (Author, "author_id"), (Role, "role_id"))
    for model, fk in foreign_keys:
        if fk in data:
            fk_id = data[fk]
            if not fk_id:
                response_message.append(f'Field "{fk}" cannot be empty')
            elif not is_object_in_db(model, fk_id):
                response_message.append(f"{model.get_name()} with id = {fk_id} doesn't exist")

    if response_message:
        return error_response(404, response_message)

    edition_author.from_dict(data)
    db.session.commit()
    return success_response(204)


@bp.route("/edition_author/<int:id>", methods=["DELETE"])
def delete_edition_author(id):
    edition_author = EditionAuthor.query.get(id)

    if not edition_author:
        return error_response(404, f"EditionAuthor with id = {id} doesn't exist")

    db.session.delete(edition_author)
    db.session.commit()
    return success_response(204)
