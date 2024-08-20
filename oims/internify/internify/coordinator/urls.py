from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user

from internify.coordinator.controllers import view_announcements, approve_announcement, decline_announcement, view_finalized, decline_application, approve_application
from internify.models import InternshipCoordinator
from internify.utils.error import Error, ErrorType

bp = Blueprint("coordinator", __name__, url_prefix="/coordinator")

@bp.route("/", methods=["GET"])
# @jwt_required()
def announcement():
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
        return view_announcements()

@bp.route("/", methods=["POST"])
# @jwt_required()
def approve():
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
        return approve_announcement()


@bp.route("/decline", methods=["POST"])
# @jwt_required()
def decline():
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
        return decline_announcement()
    

@bp.route("/finalized", methods=["GET"])
# @jwt_required()
def view_final():
    if request.method == "GET":
        # if not isinstance(current_user, InternshipCoordinator):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Company can decline student"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return view_finalized()


@bp.route("/decline_app", methods=["POST"])
# @jwt_required()
def decline_app():
    if request.method == "POST":
        # if not isinstance(current_user, InternshipCoordinator):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Company can decline student"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return decline_application()
    
@bp.route("/approve_app", methods=["POST"])
# @jwt_required()
def approve_app():
    if request.method == "POST":
        # if not isinstance(current_user, InternshipCoordinator):
        #     return (
        #         jsonify(
        #             Error(
        #                 ErrorType.FORBIDDEN, "Only Company can decline student"
        #             ).serialize()
        #         ),
        #         403,
        #     )
        return approve_application()