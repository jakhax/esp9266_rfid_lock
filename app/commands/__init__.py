import getpass
from flask_script import Command, Manager, Option
from app.models import Admin
import click

class CreateSuperUser(Command):
    help="create admin"

    def get_pass(self):
        p1=getpass.getpass(prompt="password:")
        p2=getpass.getpass(prompt="confirm password:")
        if p2!=p1:
            click.secho("Passwords dont match",fg="red")
            self.get_pass()
        return p1

    def run(self):
        username=input("Username:")
        password=self.get_pass()
        admin=Admin.query.filter_by(username=username).first()
        if not admin:
            admin=Admin(username=username,passwd=password)
            admin.save()
            click.secho("Admin {} created".format(username),fg="green")
        else:
            click.secho("Admin with username {} already exists".format(username),fg="red")

