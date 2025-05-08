from flask import Blueprint

from .index import bp as index_bp

bp = Blueprint("app", __name__)
bp.register_blueprint(index_bp, url_prefix="/")