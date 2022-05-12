from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .routes import tasks_bp, validate_task
from app.models.goal import Goal

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        validate_task(task_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 404))
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})