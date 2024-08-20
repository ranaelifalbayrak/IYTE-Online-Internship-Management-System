from requests import Session
from flask import request, jsonify, Response
from flask_jwt_extended import current_user

from internify.models import Announcement, Company, db, RawDocuments, Student , Documents, Application
from internify.utils.file_uploder import auto_fill
from internify.utils.form_validator import validate_request_data
from internify.utils.error import Error, ErrorType




def fill_the_form():

    required_fields = {
        "company_email":str
    }

    data = request.json

    is_valid, error = validate_request_data(data, required_fields)

    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    company = db.session.scalars(db.select(Company).where(Company.email == data["company_email"])).one_or_none()
    if company is None:
        return jsonify(Error(ErrorType.NOT_FOUND, "No Such Company").serialize()), 404
    

    doc = db.session.scalars(db.select(RawDocuments).where(RawDocuments.id == 1)).one_or_none()
    
    if not doc:
        return jsonify(Error(ErrorType.NOT_FOUND, "No Such Doc").serialize()), 404
    
    try:
        company = db.session.query(Company).filter(Company.email == data["company_email"]).one_or_none()
        if company is None:
            return jsonify(Error(ErrorType.NOT_FOUND, "No Such Company").serialize()), 404
        announcement_count = db.session.query(db.func.count()).select_from(Announcement).filter(Announcement.company_id == company.id).filter(Announcement.is_checked==1).scalar()
        application_count = db.session.query(db.func.count()).select_from(Documents).filter(Documents.type == 1).filter(Documents.company_id == company.id).filter(Documents.student_id ==current_user.id).scalar()
        rejected_application_count = db.session.query(db.func.count()).select_from(Documents).filter(Documents.type == 1).filter(Documents.company_id == company.id).filter(Documents.student_id ==current_user.id).filter(Documents.state==-1).scalar()
        rejected_count = application_count- rejected_application_count
        rejected_application_by_coordinator_count = db.session.query(db.func.count()).select_from(Documents).filter(Documents.type == 1).filter(Documents.company_id == company.id).filter(Documents.student_id ==current_user.id).filter(Documents.state==-2).scalar()


        if announcement_count > 0 and application_count<1:
            auto_fill(doc, company)
            new_application = Application(
                state=0
            )
            new_application.company_id = company.id # Corrected placement
            new_application.student_id = current_user.id

            db.session.add(new_application)
            db.session.commit()
            return Response(status=200)
        
        
        elif(announcement_count > 0 and rejected_count<1):
                doc = db.session.query(Documents).filter(Documents.type == 1).filter(Documents.company_id == company.id).filter(Documents.student_id ==current_user.id).one_or_none()
                application = db.session.query(Application).filter(Application.company_id == company.id).filter(Application.student_id ==current_user.id).one_or_none()
                doc.state=0
                application.state=0
                db.session.commit()
                return Response(status=200)
        else:
        
            if announcement_count == 0:
                return jsonify(Error(ErrorType.FORBIDDEN, ("You cannot apply to a company that has no application announcements.")).serialize()), 403
            elif rejected_application_by_coordinator_count==1:
                return jsonify(Error(ErrorType.FORBIDDEN, ("You cannot apply to a company that has rejected by coordinator.")).serialize()), 403
            else:
                return jsonify(Error(ErrorType.FORBIDDEN, ("You have already applied this company.")).serialize()), 403

    except SQLAlchemyError as e: # type: ignore
        print(f"Database error occurred: {e}")
        return Response(status=500)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return Response(status=400)


def view_applications():
    documents = current_user.documents
    results = []

    for document in documents:
        company = Company.query.filter_by(id=document.company_id).first()
        if company:
            company_name = company.name
        else:
            company_name = "Unknown Company"  # Eğer şirket bulunamazsa

        # Belge bilgisini ve ilgili şirket adını sözlük yapısında saklayın
        doc_data = document.serialize()
        doc_data['company_name'] = company_name
        if((doc_data['state']==2 or doc_data['state']==3 or doc_data['state']==4) and doc_data['type']==1) :
            results= []
            results.append(doc_data)
            break
        if(doc_data['type']==1):
            results.append(doc_data)

    return jsonify({"Letters": results}), 200


def view_announcements() : 
    # Fetch unchecked announcements
    announcements = db.session.scalars(db.select(Announcement).where(Announcement.is_checked == True)).all()
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

def finalize_func():
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
    application.state=2
    doc.state= 2

    if application is None:
        return jsonify({"error": "Application not found"}), 404
    
    
    db.session.commit()
    return Response(status=200)


def update_profile():
    required_fields = {
    "extra_information":str
    }

    data = request.json
    is_valid, error = validate_request_data(data, required_fields)
    if not is_valid:
        return jsonify(Error(ErrorType.SYNTACTIC, error).serialize()), 400
    
    info = data.get("extra_information")  # Use get to avoid KeyError if 'id' is not present

    current_user.extra_informations= info
    db.session.commit()
    return Response(status=200)

