import os
import datetime as dt
from flask import (
    send_from_directory,
    render_template,
    flash,
    redirect,
    request,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddForm, EditForm
from app.models import User, Task
from config import Config
from werkzeug.utils import secure_filename


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    tasks = current_user.user_tasks()
    current_time = dt.datetime.utcnow()
    tasks_timediff = []
    for task in tasks:
        if isinstance(task.deadline, dt.datetime):
            x = task.deadline - current_time
            tasks_timediff.append((task, x.total_seconds()))
        else:
            tasks_timediff.append((task, 3600))
    count = len(tasks_timediff)
    return render_template(
        "index.html", tasks=tasks_timediff, count=count, title="Tasks Overview"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("index"))
    return render_template(
        "login.html",
        title="Log In",
        registration_allowed=Config.REGISTRATION_ALLOWED,
        form=form,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if Config.REGISTRATION_ALLOWED is False:
        flash("Registration disabled")
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Succesfuly registered! You can log in.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/addtask", methods=["GET", "POST"])
@login_required
def addtask():
    form = AddForm()
    if form.validate_on_submit():
        utc_diff = form.time_offset.data
        if form.deadline.data is not None:
            utc_time = form.deadline.data + dt.timedelta(minutes=int(utc_diff))
        else:
            utc_time = None
        if form.upload_file.data is not None:
            f = form.upload_file.data
            filename = secure_filename(f.filename)
            filename_unique = f"{dt.datetime.now().timestamp()}-{filename}"
            user_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id))
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            f.save(os.path.join(user_path, filename_unique))
        else:
            filename_unique = ""
            filename = ""
        task = Task(
            title=form.title.data,
            desc=form.desc.data,
            deadline=utc_time,
            file_path=filename_unique,
            file_name=filename,
            author=current_user,
            utc_offset=utc_diff,
        )
        db.session.add(task)
        db.session.commit()
        flash("New task added successfully")
        return render_template("task.html", title=task.title, task=task)
    return render_template("addtask.html", title="Add task", form=form)


@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_task(id):
    form = EditForm()
    task = Task.query.get(id)
    if task is None or task.author != current_user or task.finished is True:
        flash("There is no such task or is marked as finished.")
        return redirect(url_for("index"))
    if form.validate_on_submit():
        utc_diff = form.time_offset.data
        if form.deadline.data is not None:
            utc_time = form.deadline.data + dt.timedelta(minutes=int(utc_diff))
        else:
            utc_time = None
        if form.upload_file.data is not None:
            f = form.upload_file.data
            filename = secure_filename(f.filename)
            filename_unique = f"{dt.datetime.now().timestamp()}-{filename}"
            user_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id))
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            f.save(os.path.join(user_path, filename_unique))
        else:
            filename_unique = task.file_path
            filename = task.file_name
        task.title = form.title.data
        task.desc = form.desc.data
        if utc_time is not None:
            task.deadline = utc_time
        else:
            task.deadline = None
        task.file_path = filename_unique
        task.file_name = filename
        task.utc_offset = utc_diff
        db.session.commit()
        flash("Task edited")
        return redirect(url_for("task_detail", id=task.id))
    elif request.method == "GET":
        form.title.data = task.title
        form.desc.data = task.desc
        if task.deadline is not None:
            time_limit = task.deadline - dt.timedelta(minutes=task.utc_offset)
            time_limit.strftime(format="%d.%m.%Y %H:%M")
            form.deadline.data = time_limit
    return render_template("edit.html", title="Edit task", form=form, task=task)


@app.route("/uploads/<id>/<file_name>")
@login_required
def file_path(id, file_name):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such file.")
        return redirect(url_for("index"))
    file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id))
    return send_from_directory(file_path, task.file_path, download_name=task.file_name)


@app.route("/delete_file/<id>")
@login_required
def delete_file(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such file.")
        return redirect(url_for("index"))
    if task.file_path is not None and task.file_path != "":
        file_path = os.path.join(
            Config.UPLOAD_FOLDER, str(current_user.id), task.file_path
        )
        if os.path.exists(file_path):
            os.remove(file_path)
            task.file_path = None
            task.file_name = None
            db.session.commit()
            flash("Attached file deleted")
            return redirect(url_for("task_detail", id=task.id))
    flash("There is no such file to delete")
    return redirect(url_for("task_detail", id=task.id))


@app.route("/task/<id>", methods=["GET"])
@login_required
def task_detail(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such task.")
        return redirect(url_for("index"))
    return render_template("task.html", title=task.title, task=task)


@app.route("/finished/<id>", methods=["GET", "POST"])
@login_required
def task_finished(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such task.")
        return redirect(url_for("index"))
    task.mark_finished()
    db.session.add(task)
    db.session.commit()
    flash(f"Finished: {task.title}")
    return redirect(url_for("index"))


@app.route("/unfinished/<id>", methods=["GET", "POST"])
@login_required
def task_unfinished(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such task.")
        return redirect(url_for("index"))
    task.mark_unfinished()
    db.session.add(task)
    db.session.commit()
    flash("Task marked as unfinished")
    return redirect(url_for("task_detail", id=task.id))


@app.route("/finished", methods=["GET", "POST"])
@login_required
def finished_tasks():
    tasks = current_user.user_tasks_finished()
    count = tasks.count()
    return render_template(
        "finished.html", count=count, tasks=tasks, title="Finished tasks"
    )


@app.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete_task(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such task.")
        return redirect(url_for("index"))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted")
    return redirect(url_for("index"))


# error handling________________________________________________


@app.errorhandler(404)
def not_found_error(error):
    flash("Page not found or access denied")
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash("Something went wrong, try again")
    return render_template("500.html"), 500
