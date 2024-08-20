from docxtpl import DocxTemplate
import sqlite3
from flask_jwt_extended import current_user
from internify.models import db, Student, RawDocuments, Documents, Company,Application
import io

# # def auto_fill(raw_doc:RawDocuments):
# #     file = io.BytesIO(raw_doc.file)

# #     template = DocxTemplate(file)

# #     context = {"name_fill" : current_user.student_name, "class_fill":current_user.student_class, "student_id_fill": current_user.student_id,"tc_fill": current_user.national_id, "telephone_fill": current_user.phone_number,"email_fill": current_user.email}

# #     template.render(context)


# #     output_stream = io.BytesIO()
# #     template.save(output_stream)
# #     output_stream = output_stream.getvalue()
# #     new_doc = Documents(1, current_user.student_id, output_stream)

# #     db.session.add(new_doc)
# #     db.session.commit()

# # def auto_fill(raw_doc: RawDocuments, email: str):
# #     try:
# #         file_stream = io.BytesIO(raw_doc.file)
# #         template = DocxTemplate(file_stream)

# #         context = {
# #             "name_fill": current_user.student_name,
# #             "class_fill": current_user.student_class,
# #             "student_id_fill": current_user.student_id,
# #             "tc_fill": current_user.national_id,
# #             "telephone_fill": current_user.phone_number,
# #             "email_fill": current_user.email  
# #         }

# #         template.render(context)
# #         output_stream = io.BytesIO()
# #         template.save(output_stream)
# #         output_stream.seek(0)
# #         output_data = output_stream.getvalue()

# #         new_doc = Documents(type=1, student_id=current_user.student_id, mail=email, file=output_data)  # 'mail' yerine 'email' düzeltildi
# #         db.session.add(new_doc)
# #         db.session.commit()

# #         return Response(status=200)
# #     except Exception as e:
# #         print(e)
# #         return jsonify({'error': str(e)}), 400
    
def auto_fill(raw_doc:RawDocuments, company:Company):
    file = io.BytesIO(raw_doc.file)

    template = DocxTemplate(file)

    context = {"name_fill" : current_user.student_name, "class_fill":current_user.student_class, "student_id_fill": current_user.student_id,"tc_fill": current_user.national_id, "telephone_fill": current_user.phone_number,"email_fill": current_user.email}

    template.render(context)
    #template.save("sonuc.docx")


    output_stream = io.BytesIO()
    template.save(output_stream)
    output_stream = output_stream.getvalue()

    new_doc = Documents(1, current_user.id, company.id, output_stream,0)
    new_doc.internship_coordinator_email = "buketoksuzoglu@std.iyte.edu.tr"
   

    db.session.add(new_doc)
    db.session.commit()




# def file_encoder(filepath:str, filename:str):
#    conn = sqlite3.connect('instance/internify.db')
#    cursor = conn.cursor()

#    with open(filepath, 'rb') as file:
#        blob = file.read()

#    cursor.execute("INSERT INTO raw_documents (name,file) VALUES (?,?)", (filename, blob,))
#    conn.commit()

#    conn.close()

# file_encoder("docs/template2.doc", "application_form")

# def blob_to_docx(database_path, table_name, blob_column, docx_file_path):
#    # Connect to the SQLite database
#    conn = sqlite3.connect(database_path)
#    cursor = conn.cursor()

#    # Retrieve the BLOB data from the database
#    cursor.execute(f"SELECT {blob_column} FROM {table_name}")
#    blob_data = cursor.fetchone()[0]

#    # Close the database connection
#    conn.close()

#    # Write the BLOB data to a DOCX file
#    with open(docx_file_path, 'wb') as docx_file:
#        docx_file.write(blob_data)

# blob_to_docx('instance/internify.db', 'documents', 'file', 'output.docx')
