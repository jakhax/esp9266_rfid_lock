import json
import time
from . import main
from flask import jsonify,request,render_template,redirect,url_for,abort
from flask_login import login_required
from.forms import CreateUserForm, EditUserForm
from app.models import User,AccessLogs,FailedAccessLogs
from app.rfid_writer_handler import RfidWriterTcpClient

user={"uid":'8660b2cc2c039ac11c17857641e509dd'}
@main.route("/validate-pin",methods=["POST"])
def validate_pin():
    if request.is_json:data=json.loads(request.json)
    else: data=json.loads(request.data)
    print("uid" in list(data.keys()))
    if data and "uid" in list(data.keys()):
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
    return abort(400)


@main.route("/create-user",methods=["GET","POST"])
@login_required
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
@login_required
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

def write_uid(id):
    user=User.query.filter_by(id=id).first()
    if not user:abort(404)
    rfid_writer_client=RfidWriterTcpClient()
    uid=user.create_uid()
    d=rfid_writer_client.send_uid(uid)
    if d=="success":
        user.save()
        return True
    else:
        return False

@main.route("/user-profile/<int:id>",methods=["GET"])
@login_required
def user_profile(id):
    success,error=None,None
    if request.args.get("create_uid",default=False):
        if write_uid(id):
            success="Successfully wrote uid to RFID tag"
        else:
            error="Error while writing uid to RFID tag"
    user=User.query.filter_by(id=id).first()
    if not user:abort(404)
    access_logs=user.access.all()
    return render_template("./core/user_profile.html",user=user,access_logs=access_logs,success=success,error=error)


@main.route("/access-logs",methods=["GET"])
@login_required
def access_logs():
    access_logs=AccessLogs.query.all()
    return render_template("./core/access_logs.html",access_logs=access_logs)

@main.route("/invalid-access-logs",methods=["GET"])
@login_required
def invalid_access_logs():
    Invalid_access_logs=FailedAccessLogs.query.all()
    return render_template("./core/invalid_access_logs.html",Invalid_access_logs=Invalid_access_logs)


@main.route('/',methods=["GET"])
@login_required
def index():
    users=User.query.all()
    return render_template("./core/index.html",users=users)