from flask import render_template, redirect, request, jsonify, url_for
from . import courses_bp
from ..models.course_model import CourseModel

course_model = CourseModel()


@courses_bp.route('/courses')
def index():
    return render_template('layouts/courses/courses.html', title="Courses", courses=course_model.fetch_all())


@courses_bp.route('/courses/add', methods=['POST'])
def add_course():
    course_id = request.form.get('course_id')
    course_name = request.form.get('coursename')
    college = request.form.get('college')

    new_course_model = CourseModel(
        course_id=course_id,
        name=course_name,
        college=college,
    )

    new_course_model.add()

    return redirect(url_for('courses.index'))


@courses_bp.route('/courses/edit/<basis_course_id>', methods=['POST'])
def edit_course(basis_course_id):
    course_id = request.form.get('course_id')
    course_name = request.form.get('course_name')
    college = request.form.get('college')

    edit_course_model = CourseModel(
        course_id=course_id,
        name=course_name,
        college=college,
    )

    print("edit_course_model.to_dict: ", edit_course_model.to_dict())
    result = edit_course_model.edit(basis_course_id)

    if result:
        response = jsonify(
            {
                'message': 'Students updated successfully',
                'basis_id': basis_course_id,
                'updated_id': course_id}
        )
        print(response.get_json())
        return redirect(url_for('courses.index'))
    else:
        response = jsonify({'message': result, 'basis_id': basis_course_id})
        print(response.get_json())
        return response


@courses_bp.route('/courses/delete', methods=['POST'])
def delete_course():
    data = request.get_json()
    course_ids = data.get('course_ids', [])
    if not course_ids:
        return jsonify({'error': 'No course IDs provided'}), 400

    result = course_model.delete_by_ids(course_ids)

    if result:
        response = jsonify(
            {
                'message': 'Courses deleted successfully',
                'deleted_ids': course_ids
            }
        )
        print(response.get_json())
        return response
    else:
        response = jsonify({'message': result, 'deleted_ids': course_ids})
        print(response.get_json())
        return response


@courses_bp.route('/courses/get', methods=['GET'])
def get_courses():
    courses = course_model.fetch_all_courses()

    print("courses: ", courses)
    return courses
