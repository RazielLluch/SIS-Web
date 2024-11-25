from flask import render_template, redirect, request, jsonify
from . import students_bp
from ..models.student_model import StudentModel

s_model = StudentModel()


# import app.models as models
# from app.user.forms import UserForm


@students_bp.route('/students')
def index(username="user"):
    return render_template('layouts/students/students.html', title='Students', students=s_model.fetch_all())
