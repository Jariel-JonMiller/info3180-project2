"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from app import app
from flask import render_template, request, jsonify, send_file
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Post, Like, Follow
# Import check_password_hash here
from werkzeug.security import check_password_hash


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    location = data.get('location', '')  # Provide default value if not present
    # Provide default value if not present
    biography = data.get('biography', '')
    # Provide default value if not present
    profile_photo = data.get('profile_photo', '')

    # Check if required fields are present
    if not (username and password and firstname and lastname and email):
        return jsonify({'message': 'Missing required fields'}), 400

    # Create a new user
    new_user = User(username=username, password=password, firstname=firstname,
                    lastname=lastname, email=email, location=location,
                    biography=biography, profile_photo=profile_photo)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "User successfully logged in.","token": access_token})


@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'User logged out successfully'})


@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@jwt_required()
def create_post(user_id):
    current_user_id = get_jwt_identity()

    # Check if the current user is authorized to create a post for the specified user
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    # Extract photo and caption from the request JSON data
    data = request.json
    photo = data.get('photo')
    # Assuming 'description' is the field name for caption
    caption = data.get('description')

    # Create a new Post object
    new_post = Post(user_id=user_id, photo=photo, caption=caption)

    # Add the new post to the database session and commit the transaction
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Successfully created a new post"}), 201


@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_posts(user_id):
    # Retrieve the user object
    user = User.query.get(user_id)

    # Check if the user exists
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    # Retrieve the posts associated with the user
    posts = user.user_posts

    # Serialize posts into the desired JSON format
    serialized_posts = []
    for post in posts:
        serialized_post = {
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on
        }
        serialized_posts.append(serialized_post)

    return jsonify({'posts': serialized_posts})


@app.route('/api/v1/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()

    new_follow = Follow(follower_id=current_user_id, user_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "You are now following that user."}), 201

@app.route('/api/v1/posts', methods=['GET'])
def allposts():
    posts = Post.query.all()
    serialized_posts = []
    for post in posts:
        serialized_post = {
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "caption": post.caption,
            "created_on": post.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            # Assuming 'likes' is a relationship in the Post model
            "likes": len(post.likes)
        }
        serialized_posts.append(serialized_post)
    return jsonify({'posts': serialized_posts})


@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like(post_id):
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
