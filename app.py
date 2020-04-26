from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/mytodo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'mytodo'

    id = db.Column(db.Integer , primary_key=True , nullable=False)
    description = db.Column(db.String(), nullable =False)


    def __repr__(self):
        return f'<Todo {self.id} :: {self.description}>'

db.create_all()


data = Todo.query.all()

@app.route('/')
def index():
    return render_template('index.html',data=data)