from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    tasks = db.relationship("Task", backref="goal", lazy=True)

    def to_dict(self):
        tasks_list = []
        for task in self.tasks:
            tasks_list.append(task.to_dict())
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": tasks_list
        }
    def to_dict_ids_only(self):
        tasks_list = []
        for task in self.tasks:
            task_info = task.to_dict()
            tasks_list.append(task_info["id"])
        return {
            "id": self.goal_id,
            "task_ids": tasks_list
        }
