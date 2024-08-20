from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask import send_file, jsonify

from internify.student.controller import fill_the_form, view_announcements, view_applications, finalize_func, update_profile
from internify.models import Student
from internify.utils.error import Error, ErrorType



bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/", methods=["GET","POST"])
@jwt_required()
def student():
    if not isinstance(current_user, Student):
        return (
            jsonify(
                Error(
                    ErrorType.FORBIDDEN, "This endpoint only for students"
                ).serialize()
            ),
            403,
        )
    
    if request.method == "GET":
        return view_applications()
    
    elif request.method == "POST":
        return fill_the_form()
    
@bp.route("/announcement", methods=["GET"])
@jwt_required()
def announcement():
    if request.method == "GET":
        if not isinstance(current_user, Student):
            return (
                jsonify(
                    Error(
                        ErrorType.FORBIDDEN, "Only Internship Coordinator can check announcements"
                    ).serialize()
                ),
                403,
            )
        return view_announcements()
    
@bp.route("/finalize", methods=["POST"])
# @jwt_required()
def finalize():
    if request.method == "POST":
        # if not isinstance(current_user, Student):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Internship Coordinator can check announcements"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return finalize_func()

@bp.route("/profile", methods=["POST"])
@jwt_required()
def update():
    if request.method == "POST":
        if not isinstance(current_user, Student):
            return (
                jsonify(
                    Error(
                        ErrorType.FORBIDDEN, "Only Student can update profile"
                    ).serialize()
                ),
                403,
            )
        return update_profile()
