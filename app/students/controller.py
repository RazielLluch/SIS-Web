from math import ceil

import cloudinary
import cloudinary.uploader
from flask import render_template, redirect, request, jsonify, url_for, flash
from . import students_bp
from ..models.student_model import StudentModel

s_model = StudentModel()


# import app.models as models
# from app.user.forms import UserForm


# Assuming you are using SQLAlchemy and have a Student model
@students_bp.route('/students')
def index():

    page = request.args.get('page', 1, type=int)

    print("Page: ", page)

    per_page = 25  # Number of students per page

    total_pages = ceil(s_model.count_all() / per_page)  # Total pages

    if page > total_pages:
        return redirect(url_for('students.index', page=1))

    students = s_model.fetch_paginated(page, per_page)

    print("total pages", total_pages)

    print("students: ", students)

    return render_template('layouts/students/students.html',
                           students=students,
                           page=page,
                           total_pages=total_pages)

@students_bp.route('/students/add', methods=['POST'])
def add_student():
    id = request.form.get('student_id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    course = request.form.get('course')
    year = request.form.get('year')
    gender = request.form.get('gender')
    profile_picture = request.files.get('add_student_image')

    print("profile picture: ", profile_picture)
    profile_picture_url = None
    if profile_picture:
        try:
            print("trying cloudinary")
            upload_picture = cloudinary.uploader.upload(profile_picture, folder="student_profile_pictures")
            profile_picture_url = upload_picture.get('url')
            print("profile_picture_url: ", profile_picture_url)
        except Exception as e:
            print(f"Upload failed :{str(e)}")
    else:
        print("No profile picture uploaded.")

    new_student_model = StudentModel(
        student_id=id,
        firstname=firstname,
        lastname=lastname,
        course=course,
        year=year,
        gender=gender,
        profile_picture_url=profile_picture_url
    )

    try:
        new_student_model.add()
    except Exception as e:

        error_message = str(e)

        print(f"Add failed :{error_message}")

        # Check if the error message contains both 'Duplicate entry' and 'course.name'
        if 'Duplicate entry' in error_message and 'student.PRIMARY' in error_message:
            flash("Course with that name already exists")
        else:
            flash("Unexpected error")

        return redirect(url_for('students.index'))
    return redirect(url_for('students.index'))


@students_bp.route('/students/edit/<basis_student_id>', methods=['POST'])
def edit_student(basis_student_id):
    student_id = request.form.get('student_id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    course = request.form.get('course')
    year = request.form.get('year')
    gender = request.form.get('gender')
    profile_picture = request.files.get('edit_student_image')

    print("profile picture: ", profile_picture)
    profile_picture_url = None
    if profile_picture:
        try:
            print("trying cloudinary")
            upload_picture = cloudinary.uploader.upload(profile_picture, folder="student_profile_pictures")
            profile_picture_url = upload_picture.get('url')
            print("profile_picture_url: ", profile_picture_url)
        except Exception as e:
            print(f"Upload failed :{str(e)}")
    else:
        print("No profile picture uploaded.")

    edit_student_model = StudentModel(
        student_id=student_id,
        firstname=firstname,
        lastname=lastname,
        course=course,
        year=year,
        gender=gender,
        profile_picture_url=profile_picture_url
    )
    
    print("edit_student_model.to_dict: ", edit_student_model.to_dict())

    result = edit_student_model.edit(basis_student_id)

    if result == True:
        flash("Student updated successfully")
        return redirect(url_for('students.index'))
    elif 'Duplicate entry' in result and 'student.PRIMARY' in result:
        flash("Student with that ID already exists")
    else:
        flash("Unexpected error")
    return redirect(url_for('students.index'))


@students_bp.route('/students/delete', methods=['POST'])
def delete_student():
    data = request.get_json()
    student_ids = data.get('student_ids', [])
    if not student_ids:
        return jsonify({'error': 'No student IDs provided'}), 400

    result = s_model.delete_by_ids(student_ids)

    if result:
        response = jsonify(
            {
                'message': 'Students deleted successfully',
                'deleted_ids': student_ids
            }
        )
        print(response.get_json())
        return response
    else:
        response = jsonify({'message': result, 'deleted_ids': student_ids})
        print(response.get_json())
        return response

@students_bp.route('/students/upload', methods=['POST'])
def upload_photo():
    image_file = request.files['file']

    image_url = None


    # student_model = StudentModel(
    #     student_id=,
    #
    # )
