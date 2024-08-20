from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask import send_file, jsonify

from internify.secratary.controller import review_sgk_eligibles,download_documents
from internify.models import Student
from internify.utils.error import Error, ErrorType



bp = Blueprint("secratary", __name__, url_prefix="/secratary")


    
@bp.route("/", methods=["GET"])
# @jwt_required()
def review():
    if request.method == "GET":
        # if not isinstance(current_user, InternshipCoordinator):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Internship Coordinator can check announcements"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return review_sgk_eligibles()
    
@bp.route("/download", methods=["POST"])
# @jwt_required()
def download():
    if request.method == "POST":
        # if not isinstance(current_user, InternshipCoordinator):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Internship Coordinator can check announcements"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return download_documents()