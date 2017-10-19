from flask import Flask, session
from flask import render_template, request, make_response

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)  # '__main__'
app.secret_key = "jheel"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')  # www.mysite.com/api/login
def login():
    return render_template('login.html')


@app.route('/register') # www.mysite.com/api/register
def register():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login',methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email,password):
        User.login(email)
    else:
        session['email'] = None
    return render_template('profile.html', email=session['email'])


@app.route('/auth/register',methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email,password)

    return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('user_blogs.html',email=user.email,blogs=blogs)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog=Blog.from_mongo(blog_id)
    posts=blog.get_posts()
    return render_template('posts.html',blog_title=blog.title,posts=posts,blog_id=blog_id)


@app.route('/blogs/new',methods=['GET','POST'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        author_id = user._id
        blog=Blog(author=user.email,title=title,description=description,author_id=author_id)
        blog.save_to_mongo()
        return make_response(user_blogs(user._id))


@app.route('/posts/new/<string:blog_id>',methods=['GET','POST'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html',blog_id=blog_id)
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])
        post=Post(author=user.email,title=title,content=content,blog_id=blog_id)
        post.save_to_mongo()
        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run()