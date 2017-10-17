import datetime
import uuid
from src.common.database import Database

class Post(object):
    def __init__(self,blog_id,title,content,author,created_date=datetime.datetime.utcnow(),_id=None):
        self.blog_id=blog_id
        self.title=title
        self.content=content
        self.author=author
        self.created_date=created_date
        self._id=uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert('posts',self.json())

    def json(self):
        return {
            '_id':self._id,
            'title':self.title,
            'content':self.content,
            'author':self.author,
            'created_date':self.created_date,
            'blog_id':self.blog_id
        }

    @classmethod
    def from_mongo(cls,id):
        post_data=Database.find_one('posts',{'_id':id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        posts=Database.find('posts',{'blog_id':id})
        return [post for post in posts]
