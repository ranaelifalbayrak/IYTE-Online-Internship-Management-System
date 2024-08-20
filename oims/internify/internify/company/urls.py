from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from internify.company.controllers import view_applications, make_announcement, decline_student , approve_student,upload_application_form, view_finalized,download_template
from internify.models import Company
from internify.utils.error import Error, ErrorType

bp = Blueprint("company", __name__, url_prefix="/company")

@bp.route("/", methods=["GET"])
@jwt_required()
def applications():
    if request.method == "GET":
        if not isinstance(current_user, Company):
            return (
                jsonify(
                    Error(
                        ErrorType.FORBIDDEN, "Only Company can view applications"
                    ).serialize()
                ),
                403,
            )
        return view_applications()

@bp.route("/", methods=["POST"])
@jwt_required()
def announce():
    if request.method == "POST":
        if not isinstance(current_user, Company):
            return (
                jsonify(
                    Error(
                        ErrorType.FORBIDDEN, "Only Company can upload announcement"
                    ).serialize()
                ),
                403,
            )
        return make_announcement()

@bp.route("/decline", methods=["POST"])
# @jwt_required()
def decline():
    # if request.method == "POST":
    #     if not isinstance(current_user, Company):
    #         return (
    #             jsonify(
    #                 Error(
    #                     ErrorType.FORBIDDEN, "Only Company can decline student"
    #                 ).serialize()
    #             ),
    #             403,
    #         )
        return decline_student()

@bp.route("/approve", methods=["POST"])
# @jwt_required()
def approve():
    # if request.method == "POST":
    #     if not isinstance(current_user, Company):
    #         return (
    #             jsonify(
    #                 Error(
    #                     ErrorType.FORBIDDEN, "Only Company can decline student"
    #                 ).serialize()
    #             ),
    #             403,
    #         )
        return approve_student()

@bp.route("/upload", methods=["POST"])
# @jwt_required()
def upload():
    # if request.method == "POST":
    #     if not isinstance(current_user, Company):
    #         return (
    #             jsonify(
    #                 Error(
    #                     ErrorType.FORBIDDEN, "Only Company can decline student"
    #                 ).serialize()
    #             ),
    #             403,
    #         )
        return upload_application_form()

@bp.route("/finalized", methods=["GET"])
@jwt_required()
def view_final():
    if request.method == "GET":
        if not isinstance(current_user, Company):
            return (
                jsonify(
                    Error(
                        ErrorType.FORBIDDEN, "Only Company can decline student"
                    ).serialize()
                ),
                403,
            )
        return view_finalized()

@bp.route("/template", methods=["GET"])
# @jwt_required()
def download_temp():
    # if request.method == "GET":
    #     if not isinstance(current_user, Company):
    #         return (
    #             jsonify(
    #                 Error(
    #                     ErrorType.FORBIDDEN, "Only Company can decline student"
    #                 ).serialize()
    #             ),
    #             403,
    #         )
        return download_template()