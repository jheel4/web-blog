from src.common.database import Database
from src.models.blog import Blog
import uuid
from flask import session
import datetime


class User(object):
    def __init__(self, email, password, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.email = email
        self.password = password

    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one('users',{'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls,id):
        data = Database.find_one('users',{'_id':id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        # User.login_valid("jheelpatel97@gmail.com",'abc123')
        # checks whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            if user.password == password:
                return True
        else:
            return False

    @classmethod
    def register(cls,email,password):
        user=cls.get_by_email(email)
        if user is None:
            user = cls(email=email,password=password)
            user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        #login_valid has already been called
        #login will store the email in the session. Next time the user accesses the profile, they will send us the
        #unique identifier stored in their cookie and this cookie will be able to identify the session which has the
        #email which needs to be generated to load their profile
        session['email']=user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {
            'email':self.email,
            'password':self.password,
            '_id':self._id
        }

    def save_to_mongo(self):
        Database.insert('users',self.json())

    def new_blog(self,description,title):
        blog=Blog(author=self.email,description=description,title=title,author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id,title,content,date=datetime.datetime.utcnow()):
        blog=Blog.from_mongo(blog_id)
        blog.new_post(title,content,date)