from email.policy import default
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

from sqlalchemy import desc 

file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class todo(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50), nullable=False)
	description=db.Column(db.String(200), nullable=False)
	date_created=db.Column(db.DateTime, default=datetime.utcnow)


	def __repr__(self):
		return f'{self.title}-{self.description}'

	'''
	This function is used to create a new todo item.
	:return: The queries that are being returned.
	'''


@app.route("/", methods=['GET', 'POST'])
	
def home():

	'''
	This function is called when the user goes to the home page. 
	
	If the user is submitting a form (i.e. if the request method is POST), then the user is adding a new
	todo to the database. 
	
	The function then takes the title and description from the form and creates a new todo instance. 
	
	The function then adds the new todo instance to the database and commits the changes. 
	
	The function then queries the database for all todos and renders the index.html template, passing in
	the todos as a list of dictionaries. 
	
	The index.html template is then rendered with the list of todos.
	:return: The queries variable.
	'''
	if (request.method=='POST'):
		title=request.form['title']
		desc=request.form['description']
		todo_instance=todo(title=title, description=desc)
		db.session.add(todo_instance)
		db.session.commit()

	
	queries=todo.query.all()
	return render_template('index.html', queries=queries)


@app.route("/update/<int:sno>/", methods=['GET', "POST"])

def update(sno):


	'''
			This function is used to update the title and description of the task.
			
			:param sno: The id of the todo item to be updated
			:return: The updated data is being returned.
	'''


	if request.method=='POST':
		updated_title=request.form['title']
		updated_desc=request.form['description']
		updation=todo.query.filter_by(id=sno).first()
		updation.title = updated_title
		updation.description=updated_desc
		db.session.add(updation)
		db.session.commit()
		return redirect("/")

	queries=todo.query.filter_by(id=sno).first()
	return render_template('update.html', queries=queries)



@app.route("/delete/<int:sno>")
def delete(sno):
	'''
	The delete function is used to delete a particular row from the database.
	
	The delete function is called when the user clicks the delete button.
	
	The delete function takes the id of the row to be deleted as an argument.
	
	The delete function queries the database for the row with the given id.
	
	The delete function deletes the row from the database.
	
	The delete function commits the changes to the database.
	
	The delete function redirects the user to the home page.
	
	:param sno: The id of the todo item to be deleted
	:return: The redirect function is being used to redirect the user to the home page.
	'''
	queries=todo.query.filter_by(id=sno).first()
	db.session.delete(queries)
	db.session.commit()
	return redirect('/')


if __name__=="main":
	app.run(debug=True)


	