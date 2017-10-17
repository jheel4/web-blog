import uuid
from src.common.database import Database
from src.models.post import Post
import datetime

class Blog(object):
    def __init__(self,author,title,description,author_id,_id=None):
        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id
        self.author_id = author_id

    def new_post(self,title,content,date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    created_date=date,
                    author=self.author)
        post.save_to_mongo()


    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert('blogs',self.json())

    def json(self):
        return {
            '_id':self._id,
            'author':self.author,
            'title':self.title,
            'description':self.description,
            'author_id':self.id
        }

    @classmethod
    def from_mongo(cls,id):
        blog_data=Database.find_one('blogs',{'_id':id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls,id):
        blog_data = Database.find('blogs',{'author_id':id})
        return [cls(**blog) for blog in blog_data]




