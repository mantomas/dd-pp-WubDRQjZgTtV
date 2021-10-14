import datetime as dt
from flask import (
    render_template,
    flash,
    redirect,
    request,
    url_for,
    current_app,
)
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from config import Settings


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user)
        return redirect(url_for("main.index"))
    return render_template(
        "login.html",
        title="Log In",
        registration_allowed=Settings.REGISTRATION_ALLOWED,
        form=form,
    )


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if Settings.REGISTRATION_ALLOWED is False:
        flash("Registration disabled")
        return redirect(url_for("auth.login"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Succesfuly registered! You can log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


@bp.route("/index", methods=["GET", "POST"])
@bp.route("/", methods=["GET", "POST"])
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
