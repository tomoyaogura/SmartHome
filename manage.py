from flask_script import Manager, Command
from app import app, db

class InitDB(Command):
	"Initializes Database"

	def run(self):
		db.create_all()

manager = Manager(app)
manager.add_command('init_db', InitDB)

if __name__ == '__main__':
	manager.run()