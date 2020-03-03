from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class  BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "repr ==> Blog Post "+ str(self.id)

all_posts = [
        {
            'title' : 'Post 1',
            'content': 'What a wonderfulday... ',
            'author' : 'ashok'
        },
        {
            'title' : 'Post 2',
            'content': 'i too had love story... '
        }
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def hello():
    return "Hello World"

@app.route('/home/users/<string:name>/<int:id>', methods=['GET'])
def hellothere(name,id):
    return "Hello %s and your id is:%s" %(name,id)

@app.route('/posts')
def posts():
    return render_template("posts.html", posts=all_posts)

if __name__ == '__main__':
    app.run(debug=True)
