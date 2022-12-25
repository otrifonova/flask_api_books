# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Author
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/author/<int:id>", methods=["GET"])
@jwt_required()
def get_author(id):
    author = Author.query.get(id)
    if author:
        return jsonify(author.to_dict())
    else:
        return error_response(404, f"author with id = {id} doesn't exist")


@bp.route("/author", methods=["POST"])
@jwt_required()
def create_author():
    data = request.get_json() or {}

    required_fields = ("name",)
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    name = data["name"]
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_author', id=author.id)
    return response


@bp.route("/author/<int:id>", methods=["PUT"])
@jwt_required()
def update_author(id):
    author = Author.query.get(id)
    if not author:
        return error_response(404, f"Author with id = {id} doesn't exist")

    data = request.get_json() or {}
    new_name = data.get("name")
    if not new_name:
        return error_response(400, 'Field "name" is empty')

    author.name = new_name
    db.session.commit()
    return success_response(204)


@bp.route("/author/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_author(id):
    author = Author.query.get(id)

    if not author:
        return error_response(404, f"author with id = {id} doesn't exist")

    db.session.delete(author)
    db.session.commit()
    return success_response(204)
