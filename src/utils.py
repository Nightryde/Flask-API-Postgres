from datetime import date, datetime
from sqlalchemy import desc
import base64
import uuid
import jwt
import os

from .entities.entity import Session
from .entities.user import User, UserSchema
from .entities.post import Post, PostSchema
from .entities.reply import Reply, ReplySchema


# all utilities used by main
class Utils:

    SECRET_KEY = "your_secret_key"  # for jwt encoding and decoding. used by main
    UPLOAD_FOLDER = "your/image/upload/folder/here"  # location of storage folder. used by main
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "jfif"}  # allowed file upload extensions

    # returns true if the post is validated and posted to database
    def on_create_post(self, request):
        try:
            # get form data, upload file, and get image name
            # sent as FormData from frontend, because it includes an image
            json_obj = request.form
            image_filename = self.upload_file(request)  # upload file method
            user_name = json_obj["postUsername"]

            # check if no file was uploaded
            if image_filename == "" or not image_filename:
                image_filename = "space.jpg"  # set default image

            # create new post object with all the data from request
            post = Post(
                user_name=user_name,
                post_category=json_obj["postCat"],
                post_title=json_obj["postTitle"],
                post_text=json_obj["postText"],
                post_image=image_filename,
                post_date=str(date.today().strftime("%m/%d/%y")),
                post_time=str(datetime.now().strftime("%H:%M:%S"))
            )

            # write to the database
            session = Session()
            session.add(post)
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_CREATE_POST EXCEPTION: " + str(e))
            return False

    # returns true if the reply is validated and posted to database
    def on_create_reply(self, request):
        try:
            # get json data
            json_obj = request.get_json()
            post_id = json_obj["postId"]

            # create new reply object with all the data from request
            reply = Reply(
                user_name=json_obj["replyUsername"],
                post_id=post_id,
                post_category=json_obj["postCat"],
                reply_text=json_obj["replyText"],
                reply_date=str(date.today().strftime("%m/%d/%y")),
                reply_time=str(datetime.now().strftime("%H:%M:%S"))
            )

            # write to the database
            session = Session()
            session.add(reply)
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_CREATE_REPLY EXCEPTION: " + str(e))
            return False

    # returns 5 top posts and images for home page
    def on_get_home(self, request):
        try:
            # fetching from the database
            session = Session()
            post_objects = session.query(Post).order_by(desc(Post.clicks)).limit(5).all()

            # convert images to base64
            images = self.get_byte_files(post_objects)

            # transforming into custom schema objects
            p_schema = PostSchema(many=True)
            posts = p_schema.dump(post_objects)

            # close db session
            session.close()

            return posts, images

        except Exception as e:
            print("ON_GET_HOME EXCEPTION: " + str(e))
            return False, False

    # returns 10 newest posts, their replies, and their images
    def on_get_new(self):
        try:
            # fetching from the database
            session = Session()
            post_objects = session.query(Post).order_by(desc(Post.id)).limit(10).all()
            reply_objects = session.query(Reply).filter(Reply.post_id >= post_objects[-1].id).all()

            # convert images to base64
            images = self.get_byte_files(post_objects)

            # transforming into custom schema objects
            p_schema = PostSchema(many=True)
            posts = p_schema.dump(post_objects)
            r_schema = ReplySchema(many=True)
            replies = r_schema.dump(reply_objects)

            # close db session
            session.close()

            return posts, replies, images

        except Exception as e:
            print("ON_GET_NEW EXCEPTION: " + str(e))
            return False, False, False

    # returns recent 10 posts for a category, their replies, and their images
    def on_get_category(self, request):
        try:
            # get category argument from request
            category = request.args.get("cat")

            # fetching from the database
            session = Session()
            post_objects = session.query(Post).filter_by(post_category=category)\
                .order_by(desc(Post.id)).limit(10).all()
            reply_objects = []

            # get replies for the 10 posts selected
            if len(post_objects) != 0:
                reply_objects = session.query(Reply).filter_by(post_cat=category)\
                    .filter(Reply.post_id >= post_objects[-1].id).order_by(desc(Reply.id)).all()

            # convert images from posts to base64
            images = self.get_byte_files(post_objects)

            # transforming into custom schema objects
            p_schema = PostSchema(many=True)
            posts = p_schema.dump(post_objects)
            r_schema = ReplySchema(many=True)
            replies = r_schema.dump(reply_objects)

            # close db session
            session.close()

            return posts, replies, images

        except Exception as e:
            print("ON_GET_CATEGORY EXCEPTION: " + str(e))
            return False, False, False

    # returns a post, its replies, and its image
    def on_get_post(self, request):
        try:
            # get post id argument from request
            post_id = request.args.get("post")

            # fetching from the database
            session = Session()
            post_object = session.query(Post).filter_by(id=post_id)
            reply_objects = session.query(Reply).filter_by(post_id=post_id).order_by(desc(Reply.id)).all()
            # update clicks
            session.query(Post).filter_by(id=post_id).update({Post.clicks: Post.clicks + 1})

            # convert image to base64
            image = self.get_byte_files(post_object)

            # transforming into custom schema objects
            p_schema = PostSchema(many=True)
            posts = p_schema.dump(post_object)
            r_schema = ReplySchema(many=True)
            replies = r_schema.dump(reply_objects)

            # close db session
            session.commit()
            session.close()

            return posts, replies, image

        except Exception as e:
            print("ON_GET_POST EXCEPTION: " + str(e))
            return False, False, False

    # returns true if the post was reported
    def on_report_post(self, request):
        try:
            # get post_id from request
            json_obj = request.get_json()
            post_id = json_obj["post"]

            # updating post and incrementing reports
            session = Session()
            session.query(Post).filter_by(id=post_id).update({Post.reports: Post.reports + 1})
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_REPORT_POST EXCEPTION: " + str(e))
            return False

    # returns true if the reply was reported
    def on_report_reply(self, request):
        try:
            # get reply_id from request
            json_obj = request.get_json()
            reply_id = json_obj["reply"]

            # updating reply and incrementing reports
            session = Session()
            session.query(Reply).filter_by(id=reply_id).update({Reply.reports: Reply.reports + 1})
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_REPORT_REPLY EXCEPTION: " + str(e))
            return False

    # returns true if the post was deleted
    def on_delete_post(self, request):
        try:
            # get post_id and jwt_token from request
            json_obj = request.get_json()
            post_id = json_obj["post"]
            jwt_token = json_obj["user"]["token"]

            # decode jwt_token into user info
            user = jwt.decode(jwt_token, self.SECRET_KEY, algorithms=["HS256"])

            # verify user to limit access
            if user["user"] == "your_admin_username":
                # delete post and its replies from database
                session = Session()
                post = session.query(Post).filter_by(id=post_id).all()
                session.query(Post).filter_by(id=post_id).delete()
                session.query(Reply).filter_by(post_id=post_id).delete()

                # get post image name
                image_name = post[0].post_image

                # delete image from file system
                if os.path.exists(self.UPLOAD_FOLDER + "/" + image_name):
                    # protect default image
                    if image_name != "space.jpg":
                        os.remove(self.UPLOAD_FOLDER + "/" + image_name)
            else:
                return False

            # close db session
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_DELETE_POST EXCEPTION: " + str(e))
            return False

    # returns true if the reply was deleted
    def on_delete_reply(self, request):
        try:
            # get variables from request
            json_obj = request.get_json()
            reply_id = json_obj["reply"]
            jwt_token = json_obj["user"]["token"]

            # decode jwt_token into user info
            user = jwt.decode(jwt_token, self.SECRET_KEY, algorithms=["HS256"])

            # verify user
            if user["user"] == "your_admin_username":
                # delete reply from database
                session = Session()
                session.query(Reply).filter_by(id=reply_id).delete()
            else:
                return False

            # close db session
            session.commit()
            session.close()

            return True

        except Exception as e:
            print("ON_DELETE_REPLY EXCEPTION: " + str(e))
            return False

    # returns (true, user info dictionary) if user is authenticated, returns (false, "none")
    def on_user_login(self, request):
        try:
            # get username and password from request
            json_obj = request.get_json()
            username = json_obj["loginUsername"]
            password = json_obj["loginPassword"]

            # fetching from the database
            session = Session()
            user_object = session.query(User).filter_by(username=username).all()

            if user_object:
                # transforming into custom schema objects
                schema = UserSchema(many=True)
                user = schema.dump(user_object)

                if json_obj and username == user["username"] and password == user["password"]:
                    return True, {"user": username, "pass": password}

            # close db session
            session.close()

            return False, "none"

        except Exception as e:
            print("ON_USER_LOGIN EXCEPTION: " + str(e))
            return False, "none"

    # util for upload_file. check if file type is allowed
    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS

    # returns image name as uuid if image exists, or an empty string if not. uploads file to storage
    def upload_file(self, request):
        if request.method == "POST":
            # check if the post request has the file
            if "postImage" not in request.files:
                return ""

            # get file from request
            file = request.files["postImage"]
            file_type = os.path.splitext(file.filename)[1]

            if file.filename == "":
                return ""
            if file and self.allowed_file(file.filename):
                # generate unique name
                filename = secure_filename(str(uuid.uuid1()) + file_type)
                filepath = os.path.join(self.UPLOAD_FOLDER, filename)
                # save to storage
                file.save(filepath)

                return filename

        return ""

    # util for get_byte_files. returns image in base64
    def encode_image(self, path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # returns list of images in base64, gotten from an input of post_objects
    def get_byte_files(self, post_objects):
        image_names = []
        for post in post_objects:
            path = ""
            if post.post_image != "":
                path = self.UPLOAD_FOLDER + "/" + post.post_image

            image_names.append({
                "name": post.id,
                "path": path
            })

        image_bytes = []
        for image in image_names:
            filename = image["name"]
            if image["path"] != "":
                img = self.encode_image(image["path"])
                image_bytes.append({filename: img})

        return image_bytes

