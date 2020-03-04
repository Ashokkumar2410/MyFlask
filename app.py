from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import requests

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
        return "Blog Post "+ str(self.id)

# all_posts = [
#         {
#             'title' : 'Post 1',
#             'content': 'What a wonderfulday... ',
#             'author' : 'ashok'
#         },
#         {
#             'title' : 'Post 2',
#             'content': 'i too had love story... '
#         }
# ]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<name>')
def return_page_1(name):
    return redirect('/')

@app.route('/home')
def hello():
    WelcomeImage='''
            <marquee behavior="alternate" width="1200" height="1000" direction="up">
                <center>
                    <img src="https://cdn.dribbble.com/users/2322685/screenshots/6221645/welcome-dribbble.gif" width="840" height="877" alt="The Scream">
                    </center>
            </marquee> '''
    return WelcomeImage
    #'<marquee behavior="alternate" direction="up"><strong><center>Hello Flask Users!!!!!</center></strong></marquee>'

#    "Hello Flask Users!!!!!"

@app.route('/home/users/<string:name>/<int:id>', methods=['GET'])
def hellothere(name,id):
    return "Hello %s and your id is:%s" %(name,id)

@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        if not post_author:
            post_author='N/A'
        new_post = BlogPost(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html", posts=all_posts)
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':

        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)


if __name__ == '__main__':
    app.run(debug=True)
