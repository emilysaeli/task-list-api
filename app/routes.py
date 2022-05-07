from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_blueprint", __name__, url_prefix="/tasks")
def validate_task(task_id):
    try:
        task_int = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    return task

@tasks_bp.route("", methods=["POST"])
def handle_tasks_post():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
        description=request_body["description"],
        )
    except:
        abort(make_response({"details":"Invalid data"}, 400))
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify({ "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
        }
    }), 201)

@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    params = request.args
    if "title" in params:
        task_name_value = params["title"]
        tasks = Task.query.filter_by(title=task_name_value)
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

#can add 'PATCH' after 'PUT'? 
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    #this seems like a good place to refactor
    try:
        validate_task(task_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 404))
    task = Task.query.get(task_id)
    request_body = request.get_json()

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