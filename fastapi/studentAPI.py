from fastapi import FastAPI
app = FastAPI()
# Temporary in-memory student database
students = [
    {"id": 1, "name": "Mounika", "age": 22},
    {"id": 2, "name": "Reshma", "age": 23}
]
# GET - Retrieve all students
@app.get("/students")
def get_students():
    return students
# GET - Retrieve one student
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Student not found"}
# POST - Create a student
@app.post("/students")
def add_student(student: dict):
    students.append(student)
    return {"message": "Student added", "student": student}
# DELETE - Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Student deleted"}

    return {"message": "Student not found"}
