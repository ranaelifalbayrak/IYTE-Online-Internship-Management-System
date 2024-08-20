# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import Integer, String, DateTime, LargeBinary
# from sqlalchemy import ForeignKey
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
# from datetime import datetime

# from werkzeug.security import generate_password_hash

# class Base(DeclarativeBase):
#     pass

# db = SQLAlchemy(model_class=Base)

# class RawDocuments(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key = True)
#     name: Mapped[str] = mapped_column(String, unique = True)
#     file: Mapped[LargeBinary] = mapped_column(LargeBinary)

#     def __init__(self, name:str, file:LargeBinary) -> None:
#         self.name = name
#         self.file = file

#     def __repr__(self) -> str:
#         return f"id: {self.id}, Name: {self.name}"
    
#     def serialize(self) -> iter:
#         data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#         return data

# class Documents(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key = True)
#     type: Mapped[int] = mapped_column(Integer)
#     student_id: Mapped[int] = mapped_column(Integer)
#     mail: Mapped[str] = mapped_column(String)  # Adding email field with a maximum length of 255 characters
#     file: Mapped[LargeBinary] = mapped_column(LargeBinary)

#     def __init__(self, type:int, student_id:int, mail:str, file:LargeBinary) -> None: #email ekledim
#         self.type = type
#         self.student_id = student_id
#         self.mail = mail
#         self.file = file

#     def __repr__(self) -> str:
#         return f"id: {self.id}, Type: {self.type}, StudentID: {self.student_id}, Email: {self.mail}"

#     def serialize(self) -> iter:
#         data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#         return data
    
# class Company(db.Model):

#     id: Mapped[int] = mapped_column(Integer, primary_key = True)
#     name: Mapped[str] = mapped_column(String, unique = True)
#     email: Mapped[str] = mapped_column(String, unique = True)
#     password: Mapped[str] = mapped_column(String)
#     registration_date: Mapped[datetime] = mapped_column(DateTime, default = datetime.now())


#     def __init__(self, name:str, email:str, password:str) -> None:
#         self.name =  name
#         self.email = email
#         self.password = generate_password_hash(password)
    
#     def __repr__(self) -> str:
#         return f"id: {self.id}, Name: {self.name}, Email: {self.email}, Registration_Date: {self.registration_date}"
    
#     def serialize(self) -> iter:
#         data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#         data.pop("password")
#         data["registration_date"] = data["registration_date"].strftime("%Y-%m-%d %H:%M:%S")
#         return data
    
# class Student(db.Model):

#     id: Mapped[int] =  mapped_column(Integer, primary_key = True)
#     student_id: Mapped[int] = mapped_column(Integer, unique=True)
#     student_name: Mapped[str] = mapped_column(String)
#     student_class: Mapped[int] = mapped_column(Integer)
#     national_id: Mapped[int] = mapped_column(Integer)
#     phone_number: Mapped[int] = mapped_column(Integer)
#     email: Mapped[str] = mapped_column(String, unique=True)
#     password: Mapped[str] = mapped_column(String)

#     def __init__(self, id:int, student_name:str, student_id:int, student_class:int, national_id:int, phone_number:int, email:str, password:str) -> None:
#         self.id = id
#         self.student_name = student_name
#         self.student_id = student_id
#         self.student_class = student_class
#         self.national_id = national_id
#         self.phone_number = phone_number
#         self.email = email
#         self.password = generate_password_hash(password)

#     def serialize(self) -> iter:
#         data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
#         data.pop("password")
#         return data

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, LargeBinary, Boolean, Float
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from typing import List
import base64


from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class RawDocuments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String, unique = True)
    file: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __init__(self, name:str, file:LargeBinary) -> None:
        self.name = name
        self.file = file

    def __repr__(self) -> str:
        return f"id: {self.id}, Name: {self.name}"
    
    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["file"] = base64.b64encode(data["file"]).decode()

        return data

class Documents(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    type: Mapped[int] = mapped_column(Integer)
    file: Mapped[LargeBinary] = mapped_column(LargeBinary)
    state: Mapped[int] = mapped_column(Integer)

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    internship_coordinator_email : Mapped[str] = mapped_column(ForeignKey("internship_coordinator.email"))

    student: Mapped["Student"] = relationship(back_populates="documents")
    company: Mapped["Company"] = relationship(back_populates="documents")
    internship_coordinator : Mapped["InternshipCoordinator"] = relationship(back_populates="documents")

    def __init__(self, type:int, student_id:int, company_id:int, file:LargeBinary, state: int) -> None:
        self.type = type
        self.student_id = student_id
        self.company_id = company_id
        self.file = file
        self.state = state

    def __repr__(self) -> str:
        return f"id: {self.id}, Type: {self.type}, StudentID: {self.student_id}, CompanyID: {self.company_id}"

    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["file"] = base64.b64encode(data["file"]).decode()
        return data
    
class Company(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String, unique = True)
    email: Mapped[str] = mapped_column(String, unique = True)
    password: Mapped[str] = mapped_column(String)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default = datetime.now())
    location : Mapped[bool] = mapped_column(Boolean)

    documents: Mapped[List["Documents"]] = relationship(back_populates="company")
    applications: Mapped[List["Application"]] = relationship(back_populates="company")
    announcements: Mapped[List["Announcement"]] = relationship(back_populates ="company")


    def __init__(self, name:str, email:str, password:str, location : str) -> None:
        self.name =  name
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
    
    def __repr__(self) -> str:
        return f"id: {self.id}, Name: {self.name}, Email: {self.email}, Registration_Date: {self.registration_date}"
    
    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password")
        data["registration_date"] = data["registration_date"].strftime("%Y-%m-%d %H:%M:%S")
        return data

class Student(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    student_id: Mapped[int] = mapped_column(Integer, unique=True)
    student_name: Mapped[str] = mapped_column(String)
    student_class: Mapped[int] = mapped_column(Integer)
    national_id: Mapped[int] = mapped_column(Integer)
    phone_number: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String, unique=True)
    has_sgk : Mapped[bool] = mapped_column(Boolean)
    has_internship : Mapped[bool] = mapped_column(Boolean)
    password: Mapped[str] = mapped_column(String)
    grade : Mapped[int] = mapped_column(Integer)
    gpa : Mapped[float] = mapped_column(Float)
    citizienship : Mapped[bool]= mapped_column(Boolean)
    extra_informations : Mapped[str] = mapped_column(String)

    documents: Mapped[List["Documents"]] = relationship(back_populates="student")
    applications: Mapped[List["Application"]] = relationship(back_populates="student")


    def __init__(self,  student_name:str, student_id:int, student_class:int, national_id:int, phone_number:int, email:str, password:str ,has_sgk : bool , grade: int , gpa : float , has_internship: bool, citizienship) -> None:
        self.student_name = student_name
        self.student_id = student_id
        self.student_class = student_class
        self.national_id = national_id
        self.phone_number = phone_number
        self.email = email
        self.password = generate_password_hash(password)
        self.grade = grade
        self.gpa = gpa
        self.has_sgk = has_sgk
        self.has_internship = has_internship
        self.citizienship = citizienship

    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password")
        return data

class Application(db.Model):
    applicaiton_id : Mapped[int] = mapped_column(Integer,primary_key=True)
    state : Mapped[int] = mapped_column(Integer)


    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    student: Mapped["Student"] = relationship(back_populates="applications")
    company: Mapped["Company"] = relationship(back_populates="applications")

    def __init__(self, state : int)-> None :
        self.state = state

    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data

class Announcement(db.Model) :
    announcement_id : Mapped[int]= mapped_column(Integer, primary_key=True)
    is_checked : Mapped[bool] = mapped_column(Boolean)
    announcement_content : Mapped[str] = mapped_column(String)
    title : Mapped[str] = mapped_column(String)

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship(back_populates="announcements")

    def __init__(self, is_checked: bool, content : str ,title : str) -> None:
        self.is_checked = is_checked
        self.announcement_content = content
        self.title = title


    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data

class InternshipCoordinator(db.Model) :
    name : Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, primary_key=True)
    password : Mapped[str] =mapped_column(String)

    documents: Mapped[List["Documents"]] = relationship(back_populates="internship_coordinator")

    def __init__(self , name : str , email: str , password : str)-> None :
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password")
        return data

class ComputerEngineeringSecretary(db.Model) :
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String)


    def __init__(self , name : str , email: str , password : str)-> None :
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def serialize(self) -> iter:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password")
        return data
