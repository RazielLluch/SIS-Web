from flask import render_template, redirect, request, jsonify
from . import courses_bp
from ..models.course_model import CourseModel

course_model = CourseModel()


@courses_bp.route('/courses')
def index():
    return render_template('layouts/courses/courses.html', courses=course_model.fetch_all())
