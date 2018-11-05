from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = ';kaskjsgu0sgkls[wpiosdfpjifds;fas'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(420))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, owner, pub_date=None):
        self.title = title
        self.body = body
        self.owner = owner

        if pub_date is None:
            pub_date = datetime.utcnow()

        self.pub_date = pub_date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def login():
    allowed_routes = ['index', 'login', 'blog', 'signup']

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#def get_users():
 #   return User.query.all()

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="User Login", users=users)

    #blog_id = request.args.get("id")
    #if blog_id:
    #    blog_words = Blog.query.get(blog_id)
    #    return render_template('blogview.html', title="Blogs!", blog_words=blog_words) 
    #else:
    #    blogs = Blog.query.all()
    #    return render_template('blog.html', title="Get Blogs Built!", blogs=blogs)

#@app.route('/blogview', methods=['GET', 'POST'])
#def blogview():
#    return render_template('blogview

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        
        if user and user.password:
            session['username'] = username
            print(session)
            flash('Logged in')
            print(session)
            return redirect('/newpost')
        else:
            if user and user.password != password:
                flash('Your password is incorrect', 'error')
                
            else:
                flash('Username does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        new_user = User(username, password)

        username_error = ''
        password_error = ''
        verify_error = ''

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:

            if (not username) or (' ' in username):
                username_error = 'That is not a valid username'

            if (not password) or (' ' in password):
                password_error = 'That is not a valid password'

            if (verify_password != password) or (not verify_password):
                verify_error = 'Passwords do not match'

            if (not username_error) and (not password_error) and (not verify_error):
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()

                session['username'] = username

                return redirect('/newpost')
            else:
                return render_template('signup.html', username=username, username_error=username_error)

    else:
        return render_template('signup.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('index')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.args.get("id"):
        blog = Blog.query.filter_by(id = request.args.get("id")).first()
        return render_template('singlePost.html', blogs=blog)
        if blog_id:
            single_post = Blog.query.get(blog_id)
            return render_template('singlePost.html', blogs=single_post)
            if author_id:
                posts_from_author = Blog.query.filter_by(owner_id=author_id)
                return render_template('singleUser.html', blogs=posts_from_author)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html', title="Make a New Post")
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_entry = request.form['entry']
        owner = User.query.filter_by(username=session['username']).first()
        blog = Blog(blog_title, blog_entry, owner, pub_date=None)
        title_error = ''
        entry_error = ''
        if len(blog_title) < 1:
            title_error = "Please write something in the title!"
        if len(blog_entry) < 1:
            entry_error = "Please write something in the entry!"
        if not title_error and not entry_error:
            blog_words = Blog(blog_title, blog_entry, owner, pub_date=None)
            db.session.add(blog_words)
            db.session.commit()
            return redirect('/blog?id={0}'.format(blog_words.id))
        else:
            return render_template('newpost.html', title="Make a New Post", title_error=title_error, entry_error=entry_error)

if __name__ == '__main__':
    app.run()