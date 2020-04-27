from flask import Flask, render_template,request,redirect,url_for ,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/mytodo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={'expire_on_commit': False})
 
#migration
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer , primary_key=True , nullable=False)
    description = db.Column(db.String(), nullable =False)
    completed = db.Column(db.Boolean(),nullable=False, default= False)
    def __repr__(self):
        return f'<Todo {self.id} :: {self.description}>'

#db.create_all() ( not used anymore as we use migrations)

# data = Todo.query.all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)

    
    # description = request.form.get('description','')
    # return redirect(url_for('index'))
 

@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())