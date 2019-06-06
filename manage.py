from app import create_app,db
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand
from app.commands import CreateSuperUser

app=create_app("development")

manager=Manager(app)
server=manager.add_command("runserver",Server(host="0.0.0.0",port=5000,use_debugger=True))

migrate=Migrate(app,db)
manager.add_command("db",MigrateCommand)

manager.add_command("createsuperuser",CreateSuperUser)


if __name__=="__main__":
    manager.run()
