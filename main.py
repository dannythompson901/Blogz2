from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blog@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.secret_key = 'wakaflaka123'
db = SQLAlchemy(app)

#Create a class for each blog post with Id, title, Body
class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

#Connects to the database
@app.before_request
def require_login():
    allowed_routes = ['index', 'blog', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')



@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #returns and displays all the blog posts
    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)
    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

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

        if len(title) > 3 and len(body) > 3:
            owner = User.query.filter_by(email=session['email']).first()
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()
            id = str(new_entry.id)
            return redirect('/blog?id=' +id)


    return render_template('newpost.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    email_error = ''
    password_error = ''
    verify_error = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if '@' not in email or ' ' in email or len(email) < 5:
            email_error = 'not a valid email address'
        if ' ' in password or len(password) < 3:
            password_error = 'not a valid password'
        if password != verify:
            verify_error = 'Passwords do not match'
        
        if email_error or password_error or verify_error:
            return render_template('signup.html', email = email, email_error=email_error, password_error=password_error, verify_error=verify_error)
        
        exist = User.query.filter_by(email=email).first()
        if exist:
            username_error = 'That username already exists'
            return render_template('signup.html', email_error=email_error, password_error=password_error, verify_error=verify_error)
        
        if not exist:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
    

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    email_error = ''
    password_error = ''
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()

        if user and user.password == password:
            session['email'] = email
            return redirect('/newpost')

        if not email:
            email_error = 'User not found'
            return render_template('login.html', email_error=email_error, password_error=password_error)

        if user.password != password:
            password_error = 'Incorrect password'
            return render_template('login.html', email_error=email_error, password_error=password_error)

    return render_template('login.html', email_error=email_error, password_error=password_error)


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


if __name__ == '__main__':
    app.run()
