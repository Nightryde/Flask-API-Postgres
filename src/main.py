from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from .entities.entity import Base, engine
from .utils import Utils
import jwt

# startup utils for use
utils = Utils()

# setup flask and CORS (cross-origin resource sharing)
app = Flask(__name__)
app.config["SECRET_KEY"] = utils.SECRET_KEY  # key for jwt
app.config["UPLOAD_FOLDER"] = utils.UPLOAD_FOLDER  # folder to store images
CORS(app)

Base.metadata.create_all(engine)  # generate database schema


@app.route("/new_post", methods=["POST"])
def create_new_post():
    # returns true if post was created, false if something went wrong
    res = utils.on_create_post(request)
    return jsonify({"response": res})


@app.route("/new_reply", methods=["POST"])
def create_new_reply():
    # returns true if reply was created, false if something went wrong
    res = utils.on_create_reply(request)
    return jsonify({"response": res})


@app.route("/get_home")
def get_home():
    # return top 5 posts and their images in base64
    posts, images = utils.on_get_home(request)
    return jsonify(posts=posts, images=images)


@app.route("/get_new")
def get_new():
    # returns new 10 posts and their replies, with the post images in base64
    posts, replies, images = utils.on_get_new()
    return jsonify(posts=posts, replies=replies, images=images)


@app.route("/get_category")
def get_category():
    # returns most recent 10 posts and their replies, with the post images in base64
    posts, replies, images = utils.on_get_category(request)
    return jsonify(posts=posts, replies=replies, images=images)


@app.route("/get_post")
def get_post():
    # returns a post and its replies, with the post image in base64
    post, replies, image = utils.on_get_post(request)
    return jsonify(post=post, replies=replies, image=image)


@app.route("/report_post", methods=["POST"])
def report_post():
    # returns true if post was reported, false if something went wrong
    res = utils.on_report_post(request)
    return jsonify({"response": res})


@app.route("/report_reply", methods=["POST"])
def report_reply():
    # returns true if reply was reported, false if something went wrong
    res = utils.on_report_reply(request)
    return jsonify({"response": res})


@app.route("/delete_post", methods=["POST"])
def delete_post():
    # returns true if post was deleted, false if something went wrong
    res = utils.on_delete_post(request)
    return jsonify({"response": res})


@app.route("/delete_reply", methods=["POST"])
def delete_reply():
    # returns true if reply was deleted, false if something went wrong
    res = utils.on_delete_reply(request)
    return jsonify({"response": res})


@app.route("/user_login", methods=["POST"])
def user_login():
    # returns json web token to be stored in browser sessionStorage
    tf, user = utils.on_user_login(request)
    # tf = true or false depending on success of user login
    if tf:
        token = jwt.encode(user, app.config["SECRET_KEY"])
        return jsonify({"token": token})
    else:
        return make_response("Could not verify", 401)

