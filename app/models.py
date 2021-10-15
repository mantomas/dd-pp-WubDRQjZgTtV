from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship("Task", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def user_tasks(self):
        tasks = Task.query.filter_by(user_id=self.id, finished=False)
        return tasks.order_by(Task.timestamp.desc())

    def user_tasks_finished(self):
        tasks = Task.query.filter_by(user_id=self.id, finished=True)
        return tasks.order_by(Task.timestamp.desc())


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    desc = db.Column(db.String(500))
    file_path = db.Column(db.String(140))
    file_name = db.Column(db.String(140))
    deadline = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    finished = db.Column(db.Boolean, default=False)
    finished_time = db.Column(db.DateTime)
    utc_offset = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Task {self.title}>"

    def mark_finished(self):
        self.finished = True
        self.finished_time = datetime.utcnow()

    def mark_unfinished(self):
        self.finished = False


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
