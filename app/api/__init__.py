from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api.routes import author, book, edition_author, edition, language, publisher, role, user
