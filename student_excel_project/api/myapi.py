
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from connect_db import SessionLocal
from typing import List
import models
import uvicorn

class Student(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    tuition_paid: bool
    class Config:
        orm_mode = True

db=SessionLocal()


app = FastAPI()

@app.get("/")
def root():
    return {"message":"welcome"}


@app.get('/students', response_model=List[Student], status_code=status.HTTP_200_OK)
def get_all_students():
    students = db.query(models.Student).all()
    return students

@app.get('/student/{student_id}',response_model=Student, status_code=status.HTTP_200_OK)
def get_a_student(student_id: int):
    retrieve_student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if retrieve_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This student does not exist.")

    return retrieve_student

@app.post('/students',response_model=Student, status_code=status.HTTP_201_CREATED)
def create_a_student(student: Student):
    new_student = models.Student(
        id= student.id,
        first_name= student.first_name,
        last_name= student.last_name,
        email= student.email,
        tuition_paid = student.tuition_paid
    )

    db_student = db.query(models.Student).filter(models.Student.id == student.id).first()
    db_email = db.query(models.Student).filter(models.Student.email == student.email).first()
    if db_student is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A student with this id already exists")

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A student with this email already exists")

    db.add(new_student)
    db.commit()
    return new_student

@app.put('/student/{student_id}',response_model=Student, status_code=status.HTTP_200_OK)
def update_a_student(student_id:int, student: Student):
    student_to_update = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This student does not exist.")

    student_to_update.id = student.id
    student_to_update.first_name = student.first_name
    student_to_update.last_name = student.last_name
    student_to_update.email = student.email
    student_to_update.tuition_paid = student.tuition_paid

    db.commit()
    return student_to_update

@app.delete('/student/{student_id}', response_model=Student, status_code=status.HTTP_200_OK)
def delete_a_student(student_id: int):
    student_to_delete = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This student does not exist.")

    db.delete(student_to_delete)
    db.commit()

    return student_to_delete


uvicorn.run(app=app, host="127.0.0.1",port=8555)
