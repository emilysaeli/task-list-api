from flask import Blueprint

tasks_bp = Blueprint("tasks_blueprint", __name__, url_prefix="/tasks")