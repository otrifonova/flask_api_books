# -*- coding: utf-8 -*-
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app import db
from app.api import bp
from app.models import Role
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/role/<int:id>", methods=["GET"])
@jwt_required()
def get_role(id):
    role = Role.query.get(id)
    if role:
        return jsonify(role.to_dict())
    else:
        return error_response(404, f"role with id = {id} doesn't exist")


@bp.route("/role", methods=["POST"])
@jwt_required()
def create_role():
    data = request.get_json() or {}

    required_fields = ("name",)
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    name = data["name"]
    role = Role.query.filter_by(name=name).first()
    if role:
        response = error_response(409, f'Role "{name}" already exist')
        response.headers['Location'] = url_for('api.get_role', id=role.id)
        return response

    role = Role(name=name)
    db.session.add(role)
    db.session.commit()

    response = success_response(201)
    response.headers['Location'] = url_for('api.get_role', id=role.id)
    return response


@bp.route("/role/<int:id>", methods=["PUT"])
@jwt_required()
def update_role(id):
    role = Role.query.get(id)
    if not role:
        return error_response(404, f"Role with id = {id} doesn't exist")

    data = request.get_json() or {}
    new_name = data.get("name")
    if not new_name:
        return error_response(400, 'Field "name" is empty')

    role.name = new_name
    db.session.commit()
    return success_response(204)


@bp.route("/role/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_role(id):
    role = Role.query.get(id)

    if not role:
        return error_response(404, f"role with id = {id} doesn't exist")

    db.session.delete(role)
    db.session.commit()
    return success_response(204)
