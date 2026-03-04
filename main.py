from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# home
@app.get("/")
def home():
    return {"message": "Student API Running"}

# create student
@app.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(
        name=student.name,
        course=student.course,
        age=student.age
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# get all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# get student by id
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}