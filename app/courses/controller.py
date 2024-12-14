from flask import render_template, redirect, request, jsonify, url_for
from . import courses_bp
from ..models.course_model import CourseModel

course_model = CourseModel()


@courses_bp.route('/courses')
def index():
    return render_template('layouts/courses/courses.html', title="Courses", courses=course_model.fetch_all())


@courses_bp.route('/courses/add', methods=['POST'])
def add_course():
    id = request.form.get('course_id')
    course_name = request.form.get('coursename')
    college = request.form.get('college')

    new_course_model = CourseModel(
        course_id=id,
        name=course_name,
        college=college,
    )

    new_course_model.add()

    return redirect(url_for('courses.index'))


@courses_bp.route('/courses/edit/<courseId>', methods=['POST'])
def edit_course(courseId):
    id = request.form.get('course_id')
    course_name = request.form.get('course_name')
    college = request.form.get('college')

    edit_course_model = CourseModel(
        course_id=id,
        name=course_name,
        college=college,
    )

    print("edit_course_model.to_dict: ", edit_course_model.to_dict())

    result = edit_course_model.edit(courseId)

    if result == True:
        response = jsonify({'message': 'Students updated successfully', 'updated_id': id})
        print(response.get_json())
        return redirect(url_for('students.index'))
    else:
        response = jsonify({'message': result, 'edit_id': id})
        print(response.get_json())
        return response


@courses_bp.route('/courses/delete', methods=['POST'])
def delete_course():
    data = request.get_json()
    student_ids = data.get('student_ids', [])
    if not student_ids:
        return jsonify({'error': 'No student IDs provided'}), 400

    result = s_model.delete_by_ids(student_ids)

    if result:
        response = jsonify({'message': 'Students deleted successfully', 'deleted_ids': student_ids})
        print(response.get_json())
        return response
    else:
        response = jsonify({'message': result, 'deleted_ids': student_ids})
        print(response.get_json())
        return response
