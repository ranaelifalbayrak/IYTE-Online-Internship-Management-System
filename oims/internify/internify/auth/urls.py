from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from internify.auth.controllers import login_controller, register_controller, refresh_token_controller

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        return register_controller()

@bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST": 
        return login_controller()

@bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    if request.method == "GET":
        return refresh_token_controller()
