from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
from .requests import use_header
from .routes import tasks_bp, validate_task
from app.models.goal import Goal

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    #this seems like a good place to refactor
    try:
        validate_task(task_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 404))
    task = Task.query.get(task_id)

    task.is_complete=False
    task.completed_at=None

    db.session.commit()


    return make_response(jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    #this seems like a good place to refactor
    try:
        validate_task(task_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 404))
    task = Task.query.get(task_id)

    task.is_complete=True
    task.completed_at= datetime.utcnow()

    db.session.commit()

        #calling Slack API
    slack_text = f"Someone just completed the task {task.title}"
    slack_call = use_header(slack_text)
    if slack_call == 200:
        return make_response(jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
        }), 200)
    else:
        abort(make_response({"details":"Invalid request"}, 400))
