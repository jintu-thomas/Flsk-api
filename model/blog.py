from db import db

class BlogModel(db.Model):
    __tablename__= 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(40))
    desc = db.Column(db.String(60))
    content = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')


    def __init__(self,heading,desc,content,user_id):
        self.heading = heading
        self.desc = desc
        self.content = content
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'heading': self.heading,
            'desc':self.content,
            'content': self.content,
            'user_id': self.user_id,
        }

    @classmethod
    def find_by_username(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    