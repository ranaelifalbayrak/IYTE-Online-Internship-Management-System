from flask_jwt_extended import JWTManager
from flask import jsonify

from internify.models import db, Company, Student

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user_type = jwt_data["user_type"]

    if user_type == "student":
        student:Student = db.session.scalars(db.select(Student).where(Student.id == identity)).one_or_none()
        return student

    elif user_type == "company":
        company:Company = db.session.scalars(
            db.select(Company).where(Company.id == identity)
        ).one_or_none()
        return company

    else:
        print("Check user_lookup_callback")


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed", "error": "invalid_token"}),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "message": "Request doesn't contain valid token",
                "error": "authorization_header",
            }
        ),
        403,
    )
