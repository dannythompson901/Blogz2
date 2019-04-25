from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLAlchemy_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:localhost@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

Class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('/')

@app.route('/blog')
def blog():
    return render_template('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('/blog')


app.run()
