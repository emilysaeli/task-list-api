from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import desc
from .routes import tasks_bp, validate_task
from app.models.goal import Goal

@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    params = request.args
    if "title" in params:
        task_name_value = params["title"]
        tasks = Task.query.filter_by(title=task_name_value)
    elif "sort" in params:
        sort_type = params["sort"]
        if sort_type == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        elif sort_type == "asc":
            tasks = Task.query.order_by(Task.title)
        else:
            return make_response({"details":"Invalid data"}, 400)

    else:
        tasks = Task.query.all()
        
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    return jsonify(tasks_response)
    #something something use abort to refactor? get task or abort from lesson

@tasks_bp.route("/<task_id>", methods=["GET"])
def individual_task(task_id):
    try:
        validate_task(task_id)
    except:
        abort(make_response({"details":"Invalid data"}, 404))
    task = Task.query.get(task_id)
    return { "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }