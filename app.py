from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import boto3, uuid, os
from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(500), nullable=True)

# S3 Client
s3 = boto3.client("s3", region_name=S3_REGION)

# @app.route("/")
# def index():
#     todos = Todo.query.all()
#     return render_template("index.html", todos=todos)
@app.route("/")
def index():
    try:
        todos = Todo.query.all()
    except Exception as e:
        return f"Error: {e}"
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        task = request.form["task"]

        logo_url = None
        if "logo" in request.files:
            file = request.files["logo"]
            if file.filename != "":
                file_key = f"{uuid.uuid4().hex}_{file.filename}"
                s3.upload_fileobj(file, S3_BUCKET, file_key, ExtraArgs={"ACL": "public-read"})
                logo_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"

        todo = Todo(task=task, logo_url=logo_url)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Database config example (SQLite)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# db = SQLAlchemy(app)

# # Default route
# @app.route('/')
# def home():
#     return "Welcome to My To-do App"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
