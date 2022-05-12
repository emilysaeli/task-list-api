from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import desc
from datetime import datetime
from .requests import use_header
from app.models.goal import Goal


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

import get_routes
import post_routes

# @tasks_bp.route("", methods=["POST"])
# def handle_tasks_post():
#     request_body = request.get_json()
#     try:
#         new_task = Task(title=request_body["title"],
#         description=request_body["description"],
#         )
#     except:
#         abort(make_response({"details":"Invalid data"}, 400))
#     try:
#         new_task= Task(completed_at=request_body["completed_at"],title=request_body["title"],
#         description=request_body["description"])
#         db.session.add(new_task)
#         db.session.commit()
#         return make_response(jsonify({ "task": {
#             "id": new_task.task_id,
#             "title": new_task.title,
#             "description": new_task.description,
#             "is_complete": True,
#             }
#         }), 201)
#     except:
#         db.session.add(new_task)
#         db.session.commit()
#         return make_response(jsonify({ "task": {
#             "id": new_task.task_id,
#             "title": new_task.title,
#             "description": new_task.description,
#             "is_complete": new_task.is_complete
#             }
#         }), 201)

# @tasks_bp.route("", methods=["GET"])
# def handle_tasks():
#     params = request.args
#     if "title" in params:
#         task_name_value = params["title"]
#         tasks = Task.query.filter_by(title=task_name_value)
#     elif "sort" in params:
#         sort_type = params["sort"]
#         if sort_type == "desc":
#             tasks = Task.query.order_by(desc(Task.title))
#         elif sort_type == "asc":
#             tasks = Task.query.order_by(Task.title)
#         else:
#             return make_response({"details":"Invalid data"}, 400)

#     else:
#         tasks = Task.query.all()
        
#     tasks_response = []
#     for task in tasks:
#         tasks_response.append({
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.is_complete
#         })
#     return jsonify(tasks_response)
#     #something something use abort to refactor? get task or abort from lesson

# @tasks_bp.route("/<task_id>", methods=["GET"])
# def individual_task(task_id):
#     try:
#         validate_task(task_id)
#     except:
#         abort(make_response({"details":"Invalid data"}, 404))
#     task = Task.query.get(task_id)
#     return { "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.is_complete
#         }
#     }


# @tasks_bp.route("/<task_id>", methods=["PUT"])
# def update_task(task_id):
#     try:
#         validate_task(task_id)
#     except: 
#         abort(make_response({"details":"Invalid data"}, 404))
#     task = Task.query.get(task_id)
#     request_body = request.get_json()
#     try:
#         task.completed_at =request_body["completed_at"]
#         task.title=request_body["title"]
#         task.description=request_body["description"]

#         db.session.commit()
#         return make_response(jsonify({ "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True
#             }
#         }), 200)

#     except:
#         task.title=request_body["title"]
#         task.description=request_body["description"]

#         db.session.commit()
#         return make_response(jsonify({ "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": task.is_complete
#             }
#         }), 200)
        
# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_task_incomplete(task_id):
#     #this seems like a good place to refactor
#     try:
#         validate_task(task_id)
#     except: 
#         abort(make_response({"details":"Invalid data"}, 404))
#     task = Task.query.get(task_id)

#     task.is_complete=False
#     task.completed_at=None

#     db.session.commit()


#     return make_response(jsonify({
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.is_complete
#         }
#     }), 200)

# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     #this seems like a good place to refactor
#     try:
#         validate_task(task_id)
#     except: 
#         abort(make_response({"details":"Invalid data"}, 404))
#     task = Task.query.get(task_id)

#     task.is_complete=True
#     task.completed_at= datetime.utcnow()

#     db.session.commit()

#         #calling Slack API
#     slack_text = f"Someone just completed the task {task.title}"
#     slack_call = use_header(slack_text)
#     if slack_call == 200:
#         return make_response(jsonify({
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": task.is_complete
#             }
#         }), 200)
#     else:
#         abort(make_response({"details":"Invalid request"}, 400))


# @tasks_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     try:
#         validate_task(task_id)
#     except: 
#         abort(make_response({"details":"Invalid data"}, 404))
#     task = validate_task(task_id)

#     db.session.delete(task)
#     db.session.commit()

#     return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})