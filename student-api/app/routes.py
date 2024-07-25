from flask import Blueprint, request, jsonify
from .models.py import Student, db

student_bp = Blueprint('student', __name__)


@student_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201


@student_bp.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    result = [{"id": student.id, "name": student.name,
               "age": student.age, "grade": student.grade} for student in students]
    return jsonify(result), 200


@student_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    result = {"id": student.id, "name": student.name,
              "age": student.age, "grade": student.grade}
    return jsonify(result), 200


@student_bp.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get_or_404(id)
    student.name = data['name']
    student.age = data['age']
    student.grade = data['grade']
    db.session.commit()
    return jsonify({"message": "Student updated successfully"}), 200


@student_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200


@student_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200
