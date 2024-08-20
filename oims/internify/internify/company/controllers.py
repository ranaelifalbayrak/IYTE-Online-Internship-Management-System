import base64
from xml.dom.minidom import Document
from flask import request
from flask import jsonify
from flask_jwt_extended import current_user

from internify.utils.form_validator import validate_request_data
from internify.models import db, Documents, Company, Announcement,Student,Application, RawDocuments
from internify.utils.error import Error, ErrorType


def view_applications():
    documents = current_user.documents
    student_ids = {doc.student_id for doc in documents}  # Unique student_ids
    students = Student.query.filter(Student.id.in_(student_ids)).all()  # Fetch all relevant students
    # Create a dictionary mapping student IDs to serialized student data instead of just names
    student_dict = {student.id: student.serialize() for student in students}

    results = []
    for document in documents:
        student_data = student_dict.get(document.student_id, {"student_name": "Unknown Student"})
        doc_data = document.serialize()
        doc_data.update(student_data)  # Merge student data into doc_data
        if doc_data['state'] == 0 and doc_data['type'] == 1:
            results.append(doc_data)

    return jsonify({"Letters": results}), 200


def view_finalized():
    documents = current_user.documents
    student_ids = {doc.student_id for doc in documents}  # Set yapısıyla unique student_id'leri toplayın
    students = Student.query.filter(Student.id.in_(student_ids)).all()  # İlgili tüm öğrencileri çekin
    student_dict = {student.id: student.student_name for student in students}  # Öğrenci id'lerini anahtar olarak kullanarak bir sözlük oluşturun

    results = []
    for document in documents:
        student_name = student_dict.get(document.student_id, "Unknown Student")
        doc_data = document.serialize()
        doc_data['student_name'] = student_name
        if (doc_data['state']==2 and doc_data['type']==1 ):
            results.append(doc_data)


    return jsonify({"Letters": results}), 200

def make_announcement(): 
    data = request.json
    try:
        new_announcement = Announcement(
            title=data["title"],
            content=data["content"],
            is_checked=False
        )
        new_announcement.company_id = current_user.id  # Corrected placement

        db.session.add(new_announcement)
        db.session.commit()

        return jsonify({"announcement": new_announcement.serialize()}), 201

    except KeyError as e:
        return jsonify({"error": str(e) + " field is missing"}), 400
    except Exception as e:
        return jsonify({"error": "DB Error Occurred", "details": str(e)}), 500
    
def decline_student():
    required_fields = {
    "id":int,
    "cid":int
    }

    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    id = data.get("id")  # Use get to avoid KeyError if 'id' is not present
    cid = data.get("cid")
    
    # Fetch the announcement by ID
    application = db.session.query(Application).filter(Application.company_id == cid).filter(Application.student_id == id).one_or_none()
    doc = db.session.query(Documents).filter(Documents.student_id == id ).filter(Documents.company_id == cid).filter(Documents.type==1).one_or_none()

    # Check if announcement exists
    application.state=-1
    doc.state= -1

    if application is None:
        return jsonify({"error": "Application not found"}), 404
    
    
    db.session.commit()
    return jsonify({"message": "Student is declined."}), 200


def approve_student():
    required_fields = {
    "id":int,
    "cid":int
    }

    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    id = data.get("id")  # Use get to avoid KeyError if 'id' is not present
    cid = data.get("cid")
    
    # Fetch the announcement by ID
    application = db.session.query(Application).filter(Application.company_id == cid).filter(Application.student_id == id).one_or_none()
    doc = db.session.query(Documents).filter(Documents.student_id == id ).filter(Documents.company_id == cid).filter(Documents.type==1).one_or_none()

    # Check if announcement exists
    application.state=1
    doc.state= 1

    if application is None:
        return jsonify({"error": "Application not found"}), 404
    
    db.session.commit()
    return jsonify({"message": "Student is approved"}), 200

def upload_application_form():
    required_fields = {"file": str, "sid": int, "cid": int}
    data = request.json

    file_content = base64.b64decode(data['file'])
    sid = data['sid']  # Student ID
    cid = data['cid']  # Company ID

    # Create a new document instance with the decoded content
    new_doc = Documents(type=2, student_id=sid, company_id=cid, file=file_content, state=3)
    new_doc.internship_coordinator_email = "buketoksuzoglu@std.iyte.edu.tr"

    # Fetch the relevant Application and Document instances
    application = db.session.query(Application).filter_by(company_id=cid, student_id=sid).one_or_none()
    doc = db.session.query(Documents).filter_by(student_id=sid, company_id=cid, type=1).one_or_none()

    # Update the state of the application and document
    if application:
        application.state = 3
    if doc:
        doc.state = 3

    # Add the new document to the session and commit it to the database
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully"}), 200

def download_template():
    document= db.session.query(RawDocuments).filter(RawDocuments.id == 2).one_or_none()
    result= document.serialize()
    return jsonify({"Form": result}), 200

