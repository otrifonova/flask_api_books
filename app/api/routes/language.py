# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Language
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/language/<int:id>", methods=["GET"])
@jwt_required()
def get_language(id):
    language = Language.query.get(id)
    if language:
        return jsonify(language.to_dict())
    else:
        return error_response(404, f"language with id = {id} doesn't exist")


@bp.route("/language", methods=["POST"])
@jwt_required()
def create_language():
    data = request.get_json() or {}

    required_fields = ("name",)
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    name = data["name"]
    language = Language.query.filter_by(name=name).first()
    if language:
        response = error_response(409, f'Language "{name}" already exist')
        response.headers['Location'] = url_for('api.get_language', id=language.id)
        return response

    language = Language(name=name)
    db.session.add(language)
    db.session.commit()

    response = success_response(201)
    response.headers["Location"] = url_for("api.get_language", id=language.id)
    return response


@bp.route("/language/<int:id>", methods=["PUT"])
@jwt_required()
def update_language(id):
    language = Language.query.get(id)
    if not language:
        return error_response(404, f"Language with id = {id} doesn't exist")

    data = request.get_json() or {}
    new_name = data.get("name")
    if not new_name:
        return error_response(400, 'Field "name" is empty')

    language.name = new_name
    db.session.commit()
    return success_response(204)


@bp.route("/language/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_language(id):
    language = Language.query.get(id)

    if not language:
        return error_response(404, f"language with id = {id} doesn't exist")

    db.session.delete(language)
    db.session.commit()
    return success_response(204)
