from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .routes import tasks_bp, validate_task
from app.models.goal import Goal

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        validate_task(task_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 404))
    task = Task.query.get(task_id)
    request_body = request.get_json()
    try:
        task.completed_at =request_body["completed_at"]
        task.title=request_body["title"]
        task.description=request_body["description"]

        db.session.commit()
        return make_response(jsonify({ "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            }
        }), 200)

    except:
        task.title=request_body["title"]
        task.description=request_body["description"]

        db.session.commit()
        return make_response(jsonify({ "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
        }), 200)