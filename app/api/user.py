# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models import User
from app.api.responses import error_response, success_response
from app.api.validators import required_fields_in_data


@bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}

    required_fields = ["username", "email", "password"]
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    user = User(username=data["username"], email=data["email"])
    if user.exists():
        return error_response(409, "Please use a different username or email")
    else:
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return success_response(201, f"{user} was created")


@bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json() or {}

    required_fields = ["username", "password"]
    if not required_fields_in_data(data, required_fields):
        return error_response(400, f"Must include fields: {', '.join(required_fields)}")

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return error_response(401, f"User {data['username']} doesn't exist")
    elif not user.check_password(data["password"]):
        return error_response(401, f"Wrong password")
    else:
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
    return jsonify({"access_token": access_token})
