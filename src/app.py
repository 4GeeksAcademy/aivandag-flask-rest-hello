"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Post, Comment, Like, Follower, Media
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return jsonify([u.serialize() for u in all_users]), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        email=data['email'],
        password=data['password'],
        is_active=data.get('is_active', true)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/post', methods=['GEt'])
def get_post():
    posts = Post.query.all()
    return jsonify([p.serialize() for p in posts]), 200

@app.route('/posts', methods=['POST'])
def crate_post():
    data = request.json
    p = Post(
        user_id=data['user_id'],

    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.serializr()), 201

@app.route('/posts/int:post_id', methods=['DELETE'])
def delete_post(post_id):
    post =Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post eliminado exitosamente"}), 200

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.json
    c = Comment(
        post_id=data['post_id'],
        user_id=data['user_id'],
        text=data['text']
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(l.serialize()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
