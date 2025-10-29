from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

#Initialization of the application
app = Flask(__name__)
CORS(app)

#Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/tododb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Primary Key True - This is how we find a To-Do later (/api/todos/1) for example.
    text = db.Column(db.String(100), nullable=False) #nullable False - This means the string can't be empty string.
    completed = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/api/todos', methods=['GET']) #GET - Allow only reading.
def get_todos():
    todos = Todo.query.all() #To-do.query - Ask the database, .all() - Give me all of them.
    todos_list = []
    for task in todos:
        todo_dictionary = {
            'id': task.id,
            'text': task.text,
            'completed': task.completed,
        }
        todos_list.append(todo_dictionary)
    return jsonify(todos_list)

@app.route('/api/todos', methods=['POST']) #POST - Create something new.
def add_todo():
    data = request.get_json()
    new_todo = Todo(text=data['text'], completed=False)
    db.session.add(new_todo) #Insert the new_todo into the database.
    db.session.commit() #Saves the database.
    return jsonify({
        'id': new_todo.id,
        'text': new_todo.text,
        'completed': new_todo.completed
    })

@app.route('/api/todos/<int:id>', methods=['PUT']) #gets the ID from URL: /api/todos/id
def toggle_todo(id): #When React presses the checkbox, toggle complete.
    todo = Todo.query.get_or_404(id) #Find the to-do with this ID, if not foud return ERROR 404.
    todo.completed = not todo.completed #Flips completion
    db.session.commit()
    return jsonify({
        'id': todo.id,
        'text': todo.text,
        'completed': todo.completed
    })

@app.route('/api/todos/<int:id>', methods=['DELETE']) #Delete to-do by ID.
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'success': True})


# Create tables and run database
with app.app_context(): #Scan all app models
    db.create_all() #Creates table for each model

if __name__ == '__main__':
    app.run(debug=True, port=5000)








