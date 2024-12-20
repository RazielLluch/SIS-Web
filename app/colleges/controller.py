from flask import render_template, redirect, request, jsonify, url_for, flash
from . import colleges_bp
from ..models.college_model import CollegeModel

college_model = CollegeModel()


@colleges_bp.route('/colleges')
def index():
    return render_template('layouts/colleges/colleges.html', title="Colleges", colleges=college_model.fetch_all())


@colleges_bp.route('/colleges/add', methods=['POST'])
def add_college():
    college_id = request.form.get('college_id')
    college_name = request.form.get('collegename')

    new_college_model = CollegeModel(
        college_id=college_id,
        name=college_name,
    )

    try:
        new_college_model.add()
    except Exception as e:
        print(f"Add failed :{str(e)}")

        error_message = str(e)

        # Check if the error message contains both 'Duplicate entry' and 'course.name'
        if 'Duplicate entry' in error_message and 'college.name' in error_message:
            flash("College with that name already exists")
        elif 'Duplicate entry' in error_message and 'college.PRIMARY' in error_message:
            flash("College with that ID already exists")
        else:
            flash("Unexpected error")

        return redirect(url_for('colleges.index'))

    return redirect(url_for('colleges.index'))


@colleges_bp.route('/colleges/edit/<basis_college_id>', methods=['POST'])
def edit_college(basis_college_id):
    college_id = request.form.get('college_id')
    college_name = request.form.get('college_name')

    edit_college_model = CollegeModel(
        college_id=college_id,
        name=college_name,
    )

    print("edit_college_model.to_dict: ", edit_college_model.to_dict())
    result = edit_college_model.edit(basis_college_id)

    print("result: ", result)

    if result == True:
        response = jsonify(
            {
                'message': 'Students updated successfully',
                'basis_id': basis_college_id,
                'updated_id': college_id}
        )
        print(response.get_json())
        flash("College edited successfully")
        return redirect(url_for('colleges.index'))
    if 'Duplicate entry' in result and 'college.PRIMARY' in result:
        flash("College with that ID already exists")
        return redirect(url_for('colleges.index'))
    elif 'Duplicate entry' in result and 'college.name' in result:
        flash("College with that name already exists")
    else:
        response = jsonify({'message': result, 'basis_id': basis_college_id})
        print(response.get_json())
        flash("Unexpected error")
    return redirect(url_for('colleges.index'))


@colleges_bp.route('/colleges/delete', methods=['POST'])
def delete_college():
    data = request.get_json()
    college_ids = data.get('college_ids', [])
    if not college_ids:
        return jsonify({'error': 'No college IDs provided'}), 400

    result = college_model.delete_by_ids(college_ids)

    if result:
        response = jsonify(
            {
                'message': 'Colleges deleted successfully',
                'deleted_ids': college_ids
            }
        )
        print(response.get_json())
        return response
    else:
        response = jsonify({'message': result, 'deleted_ids': college_ids})
        print(response.get_json())
        return response


@colleges_bp.route('/colleges/get', methods=['GET'])
def get_courses():
    courses = college_model.fetch_all_courses()

    return courses
