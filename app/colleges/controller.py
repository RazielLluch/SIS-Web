from flask import render_template, redirect, request, jsonify, url_for
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

    new_college_model.add()

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

    if result:
        response = jsonify(
            {
                'message': 'Students updated successfully',
                'basis_id': basis_college_id,
                'updated_id': college_id}
        )
        print(response.get_json())
        return redirect(url_for('colleges.index'))
    else:
        response = jsonify({'message': result, 'basis_id': basis_college_id})
        print(response.get_json())
        return response


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
