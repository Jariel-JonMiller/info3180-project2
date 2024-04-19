import os
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import app
from .models import db, User, Post, Like, Follow
# Import check_password_hash here
from werkzeug.security import check_password_hash




# @app.route('/api/v1/users/register', methods=['POST'])
# def register_user():
#     data = request.json
#     new_user = User(username=data['username'], password=data['password'], firstname=data['firstname'], lastname=data['lastname'], email=data['email'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User registered successfully'})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "message": "User successfully logged in."})

@app.route('/api/v1/auth/logout', methods=['POST'])
def logout_user():
    logout_user()  # Call the logout_user() function provided by Flask-Login
    return jsonify({'message': 'User logged out successfully'})


@app.route('/api/v1/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()

    new_follow = Follow(follower_id=current_user_id, user_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "You are now following that user."}), 201


@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = get_jwt_identity()

    like = Like.query.filter_by(
        post_id=post_id, user_id=current_user_id).first()
    if like:
        return jsonify({"message": "You have already liked this post"}), 400

    new_like = Like(post_id=post_id, user_id=current_user_id)
    db.session.add(new_like)
    db.session.commit()

    total_likes = Like.query.filter_by(post_id=post_id).count()

    return jsonify({"message": "Post liked!", "likes": total_likes}), 201

# Route to add a post to a user's feed


@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@jwt_required()
def create_post(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    photo = data.get('photo')
    caption = data.get('caption')

    new_post = Post(user_id=user_id, photo=photo, caption=caption)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Successfully created a new post"}), 201



# Route to get a user's posts


@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    user = User.query.get(user_id)
    posts = user.posts
    return jsonify({'posts': [post.caption for post in posts]})

# Route to get all posts for all users


@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.caption for post in posts]})

# The functions below should be applicable to all Flask apps

# Define a function to collect form errors from Flask-WTF


def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = f"Error in the {getattr(form, field).label.text} field - {error}"
            error_messages.append(message)
    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
