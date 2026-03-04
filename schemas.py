from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    course: str
    age: int

class Student(StudentCreate):
    id: int

    class Config:
        orm_mode = True