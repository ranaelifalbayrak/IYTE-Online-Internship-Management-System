from requests import Session
from flask import request, jsonify, Response
from flask_jwt_extended import current_user

from internify.models import Announcement, Company, db, RawDocuments, Student , Documents, Application
from internify.utils.file_uploder import auto_fill
from internify.utils.form_validator import validate_request_data
from internify.utils.error import Error, ErrorType
from flask import jsonify




def review_sgk_eligibles():
    documents = Documents.query.where(Documents.type==1 and Documents.student_id).all()
    student_ids = {doc.student_id for doc in documents}  # Set yapısıyla unique student_id'leri toplayın
    students = Student.query.filter(Student.id.in_(student_ids)).all()  # İlgili tüm öğrencileri çekin
    student_dict = {student.id: student.student_name for student in students}  # Öğrenci id'lerini anahtar olarak kullanarak bir sözlük oluşturun
    documents2 = Documents.query.filter(Documents.type == 2, Documents.state == 4).\
                                join(Student, Student.id == Documents.student_id).\
                                filter(Student.citizienship == True).\
                                filter(Student.has_sgk == False).\
                                join(Company, Company.id == Documents.company_id).\
                                filter(Company.location== True).\
                                all()

    results = []
    for document in documents2:
        student_name = student_dict.get(document.student_id, "Unknown Student")
        doc_data = document.serialize()
        doc_data['student_name'] = student_name
        results.append(doc_data)



    return jsonify({"Letters": results}), 200


def download_documents():
    required_fields = {"id": int, "cid": int}
    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify({"error": error}), 400

    student_id = data.get("id")  # Use get to avoid KeyError if 'id' is not present
    company_id = data.get("cid")

    # Fetch the student
    student = Student.query.filter_by(id=student_id).one_or_none()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Fetch documents
    document1 = Documents.query.filter_by(type=1, company_id=company_id, student_id=student_id).one_or_none()
    document2 = Documents.query.filter_by(type=2, company_id=company_id, student_id=student_id).one_or_none()

    # Serialize documents
    if document1:
        doc1_data = document1.serialize()
        doc1_data['student_name'] = student.student_name
    else:
        doc1_data = "No document found"
    
    if document2:
        doc2_data = document2.serialize()
        doc2_data['student_name'] = student.student_name
    else:
        doc2_data = "No document found"

    return jsonify({"Letter": doc1_data, "Form": doc2_data}), 200
