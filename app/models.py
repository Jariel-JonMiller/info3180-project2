from datetime import datetime
from werkzeug.security import generate_password_hash
from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(), nullable=False)
    biography = db.Column(db.String(), nullable=False)
    profile_photo = db.Column(db.String(), nullable=False)
    joined_on = db.Column(db.DateTime(), nullable=False)
    # Changed back reference name to 'author'
    user_posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(500))
    photo = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, user_id, photo, caption ):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
        self.created_on = datetime.now()


    def __repr__(self):
	    return '<Posts %r>' % (self.id)


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('likes', lazy=True))
    user = db.relationship('User', backref=db.backref('likes', lazy=True))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return '<Like %r>' % self.id


class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower = db.relationship('User', foreign_keys=[
                               follower_id], backref=db.backref('following', lazy='dynamic'))
    user = db.relationship('User', foreign_keys=[
                           user_id], backref=db.backref('followers', lazy='dynamic'))

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id

    def __repr__(self):
        return '<Follow %r>' % self.id
