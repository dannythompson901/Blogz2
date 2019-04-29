from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:localhost@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#Connects to the database


#Create a class for each blog post with Id, title, Body
class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    

#index route    
@app.route('/', methods=['POST', 'GET'])
def index():
    #grabs the id from the url
    post_id = request.args.get('id')
    title = 'Build a Blog'
    #creates the default title
    posts = [] #creates the array for the posts to be put into
    if post_id:
        #if there is a post id and the query was successful
        posts = Blog.query.filter_by(id=post_id).all() #grab the blog post with the id
        title = Blog.title #grabs the title of the blog post
        return render_template('post.html', title = title, posts = posts, id = id) #returns the template with single page post
    return redirect('/blog') #if not, returns the blog page with all the posts


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #returns and displays all the blog posts
    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ''
    text_error = ''
    #if it is a post method, it grabs the title and body 
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title_error = 'You need to have a title!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)
        if not body:
            text_error = 'You need to add content!'
            return render_template('newpost.html', title_error = title_error, text_error = text_error)
        #checks to see if there is a tile and body 
        new_post = Blog(title, body)
        posts = [new_post]
        
        title = new_post.title
        body = new_post.body
        #adds and commits the new post to the database
        db.session.add(new_post)
        db.session.commit()

        return render_template('post.html', title = title, body=body, posts = posts)
    return render_template('newpost.html', title_error = title_error, text_error = text_error)
if __name__ == '__main__':
    app.run()
