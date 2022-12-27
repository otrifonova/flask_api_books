# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import ModelGetter
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data, validate_foreign_keys


@bp.route("/<entity>/<int:id>", methods=["GET"])
@jwt_required()
def get_entity(entity, id):
    record = ModelGetter.get_model(entity).query.get(id)
    if record:
        return jsonify(record.to_dict())
    else:
        return error_response(404, f"{entity} with id = {id} doesn't exist")


@bp.route("/<entity>", methods=["POST"])
@jwt_required()
def create_entity(entity):
    data = request.get_json() or {}

    required_fields = ModelGetter.get_model(entity).get_required_fields()
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    response_message = validate_foreign_keys(entity, data)
    if response_message:
        return error_response(404, response_message)

    if entity == "edition":
        edition = ModelGetter.get_model(entity).query.filter_by(isbn=data["isbn"]).first()
        if edition:
            response = error_response(400, f"Edition with ISBN {edition.isbn} already exists (id = {edition.id})")
            response.headers["Location"] = url_for("api.get_entity", entity=entity, id=edition.id)
            return response

    record = ModelGetter.get_model(entity)()
    record.from_dict(data)

    db.session.add(record)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_entity', entity=entity, id=record.id)
    return response


@bp.route("/<entity>/<int:id>", methods=["PUT"])
@jwt_required()
def update_author(entity, id):
    record = ModelGetter.get_model(entity).query.get(id)
    if not record:
        return error_response(404, f"{entity} with id = {id} doesn't exist")

    data = request.get_json() or {}

    response_message = validate_foreign_keys(entity, data)
    if response_message:
        return error_response(404, response_message)

    if entity == "edition" and "isbn" in data:
        edition = ModelGetter.get_model(entity).query.filter_by(isbn=data["isbn"]).first()
        if id != edition.id:
            response = error_response(400, f"Edition with ISBN {edition.isbn} already exists (id = {edition.id})")
            response.headers["Location"] = url_for("api.get_entity", entity=entity, id=edition.id)
            return response

    record.from_dict(data)
    db.session.commit()
    return success_response(204)


@bp.route("/<entity>/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_author(entity, id):
    record = ModelGetter.get_model(entity).query.get(id)

    if not record:
        return error_response(404, f"{entity} with id = {id} doesn't exist")

    db.session.delete(record)
    db.session.commit()
    return success_response(204)
