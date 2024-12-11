from flask import render_template, redirect, request, jsonify
from . import colleges_bp
from ..models.college_model import CollegeModel

college_model = CollegeModel()


@colleges_bp.route('/colleges')
def index():
    return render_template('layouts/colleges/colleges.html', colleges=college_model.fetch_all())
