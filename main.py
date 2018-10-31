from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(420))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    blog_id = request.args.get("id")
    if blog_id:
        blog_words = Blog.query.get(blog_id)
        return render_template('blogview.html', title="Blogs!", blog_words=blog_words) 
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Get Blogs Built!", blogs=blogs)

#@app.route('/blogview', methods=['GET', 'POST'])
#def blogview():
#    return render_template('blogview
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html', title="Make a New Post")
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_entry = request.form['entry']
        title_error = ''
        entry_error = ''
        if len(blog_title) < 1:
            title_error = "Please write something in the title!"
        if len(blog_entry) < 1:
            entry_error = "Please write something in the entry!"
        if not title_error and not entry_error:
            blog_words = Blog(blog_title, blog_entry)
            db.session.add(blog_words)
            db.session.commit()
            return render_template('blogview.html', blog_words=blog_words)
        else:
            return render_template('newpost.html', title="Make a New Post", title_error=title_error, entry_error=entry_error)

if __name__ == '__main__':
    app.run()