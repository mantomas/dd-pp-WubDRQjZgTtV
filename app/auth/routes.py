from flask import (
    render_template,
    flash,
    redirect,
    request,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.forms import LoginForm, RegistrationForm
from app.models import User
from config import Config


@bp.route("/login", methods=["GET", "POST"])
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


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@bp.route("/register", methods=["GET", "POST"])
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