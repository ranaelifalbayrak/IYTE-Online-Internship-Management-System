from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
import requests
from sqlalchemy.exc import IntegrityError 


from internify.utils.form_validator import validate_request_data
from internify.utils.error import Error, ErrorType
from internify.models import db, Company, Student, InternshipCoordinator , ComputerEngineeringSecretary


MOCK_API_BASE_URL="https://66360f95415f4e1a5e2625c5.mockapi.io/internify"

def register_controller():

    required_fields = {
        "name":str,
        "email":str, 
        "password":str,
        "location":int
    }
    


    data = request.json

    is_valid, error = validate_request_data(data, required_fields)

    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    existing_user = Company.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify(Error(ErrorType.SYNTACTIC, "This account already exists.").serialize()), 409

    
    try:
        location = data["location"] == 1
        new_user = Company(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            location = location
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {"company": new_user.serialize()}
            ),
            201,
        )
    
    except:
        return (
            jsonify(
                Error(
                    ErrorType.DB_ERROR,
                    "DB Error Occured"
                ).serialize()
            ),

# def login_controller():
#     required_fields = {
#            500,
       )

def login_controller():
    required_fields = {
        "user_type":int, #1 Student, 2 Company and so on
        "email":str, 
        "password":str 
    }

    data = request.json

    is_valid, error = validate_request_data(data, required_fields)

    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400

    if data["user_type"] == 1:
        user:Student = db.session.scalars(db.select(Student).where(Student.email == data["email"])).one_or_none()

        if user is None:
            return jsonify(Error(ErrorType.NOT_FOUND, "No Such User").serialize()), 404
    
        if not check_password_hash(user.password, data["password"]):
            return jsonify(
                Error(ErrorType.SEMANTIC, "Wrong password entered").serialize()), 422

        access_token = create_access_token(identity = user.id, additional_claims = {"user_type" : "student"})
        refresh_token = create_refresh_token(identity = user.id, additional_claims = {"user_type" : "student"})

        return(
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "user_type": "company",
                        **user.serialize(),
                    },
                }
            ), 200  
        )   

        
        
        
#response_data[0]["id"], response_data[0]["student_name"], response_data[0]["student_number"], response_data[0]["email"], response_data[0]["password"]
                    

      


    elif data["user_type"] == 2:
        user:Company = db.session.scalars(db.select(Company).where(Company.email == data["email"])).one_or_none()

        if user is None:
            return jsonify(Error(ErrorType.NOT_FOUND, "No Such User").serialize()), 404
    
        if not check_password_hash(user.password, data["password"]):
            return jsonify(
                Error(ErrorType.SEMANTIC, "Wrong password entered").serialize()), 422

        access_token = create_access_token(identity = user.id, additional_claims = {"user_type" : "company"})
        refresh_token = create_refresh_token(identity = user.id, additional_claims = {"user_type" : "company"})

        return(
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "user_type": "company",
                        **user.serialize(),
                    },
                }
            ), 200  
        )  
    elif data["user_type"] == 3:
        user:InternshipCoordinator = db.session.scalars(db.select(InternshipCoordinator).where(InternshipCoordinator.email == data["email"])).one_or_none()

        if user is None:
            return jsonify(Error(ErrorType.NOT_FOUND, "No Such User").serialize()), 404
    
        if not check_password_hash(user.password, data["password"]):
            return jsonify(
                Error(ErrorType.SEMANTIC, "Wrong password entered").serialize()), 422

        access_token = create_access_token(identity = user.email, additional_claims = {"user_type" : "internship_coordinator"})
        refresh_token = create_refresh_token(identity = user.email, additional_claims = {"user_type" : "internship_coordinator"})

        return(
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "user_type": "internship_coordinator",
                        **user.serialize(),
                    },
                }
            ), 200  
        )   
    elif data["user_type"] == 4:
        user:ComputerEngineeringSecretary = db.session.scalars(db.select(ComputerEngineeringSecretary).where(ComputerEngineeringSecretary.email == data["email"])).one_or_none()

        if user is None:
            return jsonify(Error(ErrorType.NOT_FOUND, "No Such User").serialize()), 404
    
        if not check_password_hash(user.password, data["password"]):
            return jsonify(
                Error(ErrorType.SEMANTIC, "Wrong password entered").serialize()), 422

        access_token = create_access_token(identity = user.email, additional_claims = {"user_type" : "computer_engineering_secratary"})
        refresh_token = create_refresh_token(identity = user.email, additional_claims = {"user_type" : "computer_engineering_secratary"})

        return(
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "user_type": "computer_engineering_secratary",
                        **user.serialize(),
                    },
                }
            ), 200  
        )  


def refresh_token_controller():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)