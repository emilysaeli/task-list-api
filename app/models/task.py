from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    is_complete = db.Column(db.Boolean, default=False)
    #goal = db.relationship("Goal", backref="task", lazy = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

    def to_dict(self):
        if  self.goal_id:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete,
                "goal_id": self.goal_id
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }
    def to_dict_basic(self):
        return {
            "task_id": self.task_id,
            "title": self.title
        }