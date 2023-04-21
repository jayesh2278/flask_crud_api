from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/love_cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, roll_number, name):
        self.roll_number = roll_number
        self.name = name

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(roll_number=data['roll_number'], name=data['name'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully.'})

@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    output = []
    for student in students:
        student_data = {}
        student_data['id'] = student.id
        student_data['roll_number'] = student.roll_number
        student_data['name'] = student.name
        output.append(student_data)
    return jsonify({'students': output})

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    student_data = {}
    student_data['id'] = student.id
    student_data['roll_number'] = student.roll_number
    student_data['name'] = student.name
    return jsonify(student_data)

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    student.roll_number = data['roll_number']
    student.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully.'})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully.'})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
