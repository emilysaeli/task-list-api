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
    new_task = Task(title=request_body["title"],
        description=request_body["description"],
        )

    db.session.add(new_task)
    db.session.commit()
    return make_response(f"Task {new_task.title} successfully created", 201)

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
    task = validate_task(task_id)

    request_body = request.get_json()

    task.task_name=request_body["task_name"]
    task.description=request_body["description"]
    task.distance_mil_miles=request_body["distance_mil_miles"]

    db.session.commit()
    return make_response(f"task #{task.id} successfully updated")


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"task #{task.task_id} successfully deleted")