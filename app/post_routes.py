from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .routes import tasks_bp, validate_task
from app.models.goal import Goal

@tasks_bp.route("", methods=["POST"])
def handle_tasks_post():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
        description=request_body["description"],
        )
    except:
        abort(make_response({"details":"Invalid data"}, 400))
    try:
        new_task= Task(completed_at=request_body["completed_at"],title=request_body["title"],
        description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({ "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True,
            }
        }), 201)
    except:
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({ "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
            }
        }), 201)