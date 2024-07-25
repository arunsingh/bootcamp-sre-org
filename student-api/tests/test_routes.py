import unittest
from app import create_app, db
from app.models import Student
import json


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_student(self):
        response = self.client.post(
            '/api/v1/students', json={"name": "John Doe", "age": 20, "grade": "A"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Student added successfully", str(response.data))

    def test_get_all_students(self):
        response = self.client.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)

    def test_get_student(self):
        student = Student(name="John Doe", age=20, grade="A")
        with self.app.app_context():
            db.session.add(student)
            db.session.commit()
        response = self.client.get(f'/api/v1/students/{student.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", str(response.data))

    def test_update_student(self):
        student = Student(name="John Doe", age=20, grade="A")
        with self.app.app_context():
            db.session.add(student)
            db.session.commit()
        response = self.client.put(
            f'/api/v1/students/{student.id}', json={"name": "Jane Doe", "age": 21, "grade": "B"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Student updated successfully", str(response.data))

    def test_delete_student(self):
        student = Student(name="John Doe", age=20, grade="A")
        with self.app.app_context():
            db.session.add(student)
            db.session.commit()
        response = self.client.delete(f'/api/v1/students/{student.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Student deleted successfully", str(response.data))


if __name__ == '__main__':
    unittest.main()
