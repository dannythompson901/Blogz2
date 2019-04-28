from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:localhost@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
@app.route('/', methods=['POST', 'GET'])
def index():
    post_id = request.args.get('id')
    title = 'Build a Blog'
    posts = []
    if post_id:
        posts = Blog.query.filter_by(id=post_id).all()
        title = Blog.title
        return render_template('post.html', title = title, posts = posts, id = id)
    return redirect('/blog')


# @app.route('/post')
# def post():
#     post_id = request.args.get('id')
#     title = 'build a blog'
#     posts = []

#     if post_id:
#         posts = Blog.query.filter_by(id = post_id).all()
#         title = Blog.title

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    

    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ''
    text_error = ''
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title_error = 'You need to have a title!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)
        if not body:
            text_error = 'You need to add content!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)

        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

        return render_template('/', title=title,)
    return render_template('newpost.html', title_error = title_error, text_error = text_error)
if __name__ == '__main__':
    app.run()
