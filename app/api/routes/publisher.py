# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Publisher
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/publisher/<int:id>", methods=["GET"])
@jwt_required()
def get_publisher(id):
    publisher = Publisher.query.get(id)
    if publisher:
        return jsonify(publisher.to_dict())
    else:
        return error_response(404, f"Publisher with id = {id} doesn't exist")


@bp.route("/publisher", methods=["POST"])
@jwt_required()
def create_publisher():
    data = request.get_json() or {}

    required_fields = ("name",)
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    name = data["name"]
    publisher = Publisher(name=name)
    db.session.add(publisher)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_publisher', id=publisher.id)
    return response


@bp.route("/publisher/<int:id>", methods=["PUT"])
@jwt_required()
def update_publisher(id):
    publisher = Publisher.query.get(id)
    if not publisher:
        return error_response(404, f"Publisher with id = {id} doesn't exist")

    data = request.get_json() or {}
    new_name = data.get("name")
    if not new_name:
        return error_response(400, 'Field "name" is empty')

    publisher.name = new_name
    db.session.commit()
    return success_response(204)


@bp.route("/publisher/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_publisher(id):
    publisher = Publisher.query.get(id)

    if not publisher:
        return error_response(404, f"Publisher with id = {id} doesn't exist")

    db.session.delete(publisher)
    db.session.commit()
    return success_response(204)
