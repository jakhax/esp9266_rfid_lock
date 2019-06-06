import json
import time
from . import main
from flask import jsonify,request,render_template
from flask_login import login_required
from.forms import CreateUserForm


user={"uid":'8660b2cc2c039ac11c17857641e509dd'}
@main.route("/validate-pin",methods=["POST"])
def validate_pin():
    data=json.loads(request.data)
    print(data)
    if bytearray(data["uid"]).hex()==user["uid"]:
        return jsonify({"response":True})
    # counter bruteforce @todo use validation token for every device
    time.sleep(1)
    return jsonify({"response":False})


@main.route("/create-user",methods=["GET","POST"])
def create_user():
    form=CreateUserForm()
    error=False
    if form.validate_on_submit():
        if  not User.query.filter_by(email=form.email.data).first():
            user=User(email=form.email.data)
            user.create_uid()
            user.save()
        error="User with email already exists"
    return render_template("./core/")
           

        

@main.route('/',methods=["GET"])
@login_required
def index():
    return render_template("./core/index.html")