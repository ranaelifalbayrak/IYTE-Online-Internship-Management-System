from flask import request
from flask import jsonify
from flask_jwt_extended import current_user

from internify.utils.form_validator import validate_request_data
from internify.models import Application, db, Documents, Company, Announcement,Student
from internify.utils.error import Error, ErrorType


def view_announcements() : 
    # Fetch unchecked announcements
    announcements = db.session.scalars(db.select(Announcement).where(Announcement.is_checked == False)).all()
    results = []

    for announcement in announcements:
        # Fetch company details for each announcement
        company = db.session.scalars(db.select(Company).where(Company.id == announcement.company_id)).first()
        if company:
            # Prepare the data as a dictionary
            result = {
                "title": announcement.title,
                "content": announcement.announcement_content,  # adjusted attribute as per your correction
                "company_name": company.name,  # make sure these attribute names match your model's definitions
                "company_email": company.email,
                "id": announcement.announcement_id
            }
            results.append(result)

    # Return JSON response with list of results
    return jsonify(results)

def approve_announcement():
    required_fields = {
        "id":int
    }

    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    announcement_id = data.get("id")  # Use get to avoid KeyError if 'id' is not present
    
    
    # Fetch the announcement by ID
    announcement = db.session.scalars(
        db.select(Announcement).where(Announcement.announcement_id == announcement_id)
    ).one_or_none()

    # Check if announcement exists
    if announcement is None:
        return jsonify({"error": "Announcement not found"}), 404

    # Mark the announcement as checked
    announcement.is_checked = True
    db.session.commit()

    # Return a success response
    return jsonify({"success": "Announcement approved"}), 200

def decline_announcement():
    required_fields = {
        "id":int
    }

    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    announcement_id = data.get("id")  # Use get to avoid KeyError if 'id' is not present
    
    
    # Fetch the announcement by ID
    announcement = db.session.scalars(
        db.select(Announcement).where(Announcement.announcement_id == announcement_id)
    ).one_or_none()

    # Check if announcement exists
    if announcement is None:
        return jsonify({"error": "Announcement not found"}), 404
    
    db.session.delete(announcement)
    db.session.commit()
            
def view_finalized():
    documents = Documents.query.filter( Documents.type == 2).all()
    student_ids = {doc.student_id for doc in documents}  # Set yapısıyla unique student_id'leri toplayın
    students = Student.query.filter(Student.id.in_(student_ids)).all()  # İlgili tüm öğrencileri çekin
    student_dict = {student.id: student.student_name for student in students}  # Öğrenci id'lerini anahtar olarak kullanarak bir sözlük oluşturun

    results = []
    for document in documents:
        student_name = student_dict.get(document.student_id, "Unknown Student")
        doc_data = document.serialize()
        doc_data['student_name'] = student_name
        if (doc_data['state']==3 and doc_data['type']==2):
            results.append(doc_data)
    return jsonify({"Letters": results}), 200


def decline_application():
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
    doc2 = db.session.query(Documents).filter(Documents.student_id == id ).filter(Documents.company_id == cid).filter(Documents.type==2).one_or_none()

    # Check if announcement exists
    application.state=-2
    doc.state= -2
    doc2.state= -2

    if application is None:
        return jsonify({"error": "Application not found"}), 404
    
    
    db.session.commit()

    return jsonify({"success": "Aplicaiton declined"}), 200



def approve_application():
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
    doc2 = db.session.query(Documents).filter(Documents.student_id == id ).filter(Documents.company_id == cid).filter(Documents.type==2).one_or_none()

    # Check if announcement exists
    application.state=4
    doc.state= 4
    doc2.state= 4

    if application is None:
        return jsonify({"error": "Application not found"}), 404
    
    
    db.session.commit()

    return jsonify({"success": "Aplicaiton approved"}), 200