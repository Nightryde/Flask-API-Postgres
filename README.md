# Flask-API-Postgres

This is a Flask API that is used to get data from PostgreSQL for use on an Angular front end.

This project includes functionality for a social media web application.

### This project requires:
1. flask and flask_cors
2. sqlalchemy
3. marshmallow

Run the bootstrap file to start Flask. Best done in a virtual environment.

## What it does

1. Create a new post
2. Create a new reply to a post
3. Get home page (top 5 posts and their images)
4. Get new posts (recent 10 posts, their replies, and their images)
5. Get post Category (recent 10 posts for a category, their replies, and their images)
6. Get post detail (post, its replies, and its image)
7. Report posts and replies (for admin to review)
8. Delete posts and replies (for validated user)
9. User login
10. File upload to server (including unique name generation and conversion to base64)
