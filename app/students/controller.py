from flask import render_template, redirect, request, jsonify, url_for
from . import students_bp
from ..models.student_model import StudentModel

s_model = StudentModel()


# import app.models as models
# from app.user.forms import UserForm


@students_bp.route('/students')
def index():
    return render_template('layouts/students/students.html', title='Students', students=s_model.fetch_all())


@students_bp.route('/students/add', methods=['POST'])
def add_student():
    id = request.form.get('student_id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    course = request.form.get('course')
    year = request.form.get('year')
    gender = request.form.get('gender')
    # profile_picture_url = request.form.get('profile_picture_url'),

    new_student_model = StudentModel(
        student_id=id,
        firstname=firstname,
        lastname=lastname,
        course=course,
        year=year,
        gender=gender,
        # profile_picture_url=profile_picture_url,
    )

    new_student_model.add_student()

    return redirect(url_for('students.index'))
