from flask import render_template, redirect, request, jsonify, url_for, flash
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

    try:
        new_course_model.add()
    except Exception as e:
        print(f"Add failed :{str(e)}")

        error_message = str(e)

        # Check if the error message contains both 'Duplicate entry' and 'course.name'
        if 'Duplicate entry' in error_message and 'course.name' in error_message:
            flash("Course with that name already exists")
        elif 'Duplicate entry' in error_message and 'course.PRIMARY' in error_message:
            flash("Course with that ID already exists")
        else:
            flash("Unexpected error")

        return redirect(url_for('courses.index'))
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

    print("result: ", result)

    if result == True:
        flash("Course updated successfully")
    elif 'Duplicate entry' in result and 'course.PRIMARY' in result:
        flash("Course with that ID already exists")
    elif 'Duplicate entry' in result and 'course.name' in result:
        flash("Course with that name already exists")
    else:
        flash("Unexpected error")
    return redirect(url_for('courses.index'))


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

    return courses
