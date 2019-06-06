import json
import time
from . import main
from flask import jsonify,request,render_template,redirect,url_for,abort
from flask_login import login_required
from.forms import CreateUserForm, EditUserForm
from app.models import User,AccessLogs,FailedAccessLogs

user={"uid":'8660b2cc2c039ac11c17857641e509dd'}
@main.route("/validate-pin",methods=["POST"])
def validate_pin():
    data=json.loads(request.data)
    if data and "uid" in data.keys():
        if type(data["uid"])==list:
            print(data)
            user=User.query.filter_by(uid=bytearray(data["uid"]).hex()).first()
            if user:
                log=AccessLogs(user_id=user.id)
                log.save()
                return jsonify({"response":True})
            failed_log=FailedAccessLogs(attempted_uid=bytearray(data["uid"]).hex())
            failed_log.save()
            # counter bruteforce @todo use validation token for every device
            time.sleep(1)
            return jsonify({"response":True})
    return jsonif({"error":"bad request"},status=400)


@main.route("/create-user",methods=["GET","POST"])
def create_user():
    form=CreateUserForm()
    error=False
    if form.validate_on_submit():
        if  not User.query.filter_by(email=form.email.data).first():
            user=User(email=form.email.data)
            user.create_uid()
            user.save()
            return redirect(url_for('main.index'))
        error="User with email already exists"
    return render_template("./core/add_user.html",form=form,error=error)


@main.route("/edit-user/<int:id>",methods=["GET","POST"])
def edit_user(id):
    user=User.query.filter_by(id=id).first()
    if not user:abort(404)
    form=EditUserForm()
    error=False
    if form.validate_on_submit():
        if  not User.query.filter_by(email=form.email.data).first():
            user.email=form.email.data
            user.save()
            return redirect(url_for('main.user_profile',id=id))
        error="User with email already exists"
    form.email.data=user.email
    return render_template("./core/edit_user.html",form=form,error=error)


@main.route("/user-profile/<int:id>",methods=["GET"])
def user_profile(id):
    user=User.query.filter_by(id=id).first()
    if not user:abort(404)
    return render_template("./core/user_profile.html",user=user)

@main.route('/',methods=["GET"])
@login_required
def index():
    users=User.query.all()
    return render_template("./core/index.html",users=users)