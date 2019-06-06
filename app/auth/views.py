from flask import render_template,redirect,url_for
from flask_login import login_user,login_required,current_user,logout_user
from . import auth
from .forms import LoginForm
from app.models import Admin

@auth.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    error=False
    if form.validate_on_submit():
        username=form.username.data
        admin=Admin.query.filter_by(username=username).first()
        if admin and admin.verifypass(form.password.data):
            login_user(admin,form.remember.data)
            return redirect(url_for("main.index"))
        error="Wrong username or password!"
    return render_template("./auth/login.html",form=form,error=error)

@auth.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))

