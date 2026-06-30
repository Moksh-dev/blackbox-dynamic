from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader
import os


app = Flask(__name__)


# -------------------------
# CONFIG
# -------------------------

app.secret_key = "blackbox-secret-key"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blackbox.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



# -------------------------
# CLOUDINARY
# -------------------------

cloudinary.config(

    cloud_name="dnvmvfr4w",

    api_key="992199383868877",

    api_secret="f54uwtrgJztfHQnSfewHyDgdmHM"

)




# -------------------------
# DATABASE MODELS
# -------------------------


class Submission(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.String(500)
    )




class Image(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    image_url = db.Column(
        db.String(500)
    )


    caption = db.Column(
        db.String(200)
    )






# -------------------------
# HOME ARCHIVE
# -------------------------


@app.route("/")

def home():

    images = Image.query.all()


    return render_template(
        "index.html",
        images=images
    )






# -------------------------
# SUBMIT MEMORY
# -------------------------


@app.route(
    "/submit",
    methods=["GET","POST"]
)

def submit():


    if request.method == "POST":

        text = request.form["content"]


        new_submission = Submission(
            content=text
        )


        db.session.add(
            new_submission
        )

        db.session.commit()


        return redirect("/")


    return render_template(
        "submit.html"
    )






# -------------------------
# LOGIN
# -------------------------


@app.route(
    "/login",
    methods=["GET","POST"]
)

def login():


    if request.method == "POST":


        password = request.form["password"]


        if password == "admin123":

            session["admin"] = True


            return redirect("/dashboard")



    return render_template(
        "login.html"
    )






# -------------------------
# DASHBOARD
# -------------------------


@app.route("/dashboard")

def dashboard():


    if not session.get("admin"):

        return redirect("/login")



    submissions = Submission.query.all()


    images = Image.query.all()



    return render_template(

        "dashboard.html",

        submissions=submissions,

        images=images

    )








# -------------------------
# UPLOAD IMAGE
# -------------------------


@app.route(
    "/upload-image",
    methods=["POST"]
)

@app.route('/upload-image', methods=['POST'])
def upload_image():

    try:
        if 'image' not in request.files:
            return "No image found"

        image = request.files['image']

        if image.filename == '':
            return "No selected file"

        path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            image.filename
        )

        image.save(path)

        return "Upload successful"

    except Exception as e:
        return str(e)








# -------------------------
# EDIT IMAGE
# -------------------------


@app.route(
    "/edit-image/<int:id>",
    methods=["GET","POST"]
)

def edit_image(id):


    if not session.get("admin"):

        return redirect("/login")



    image = Image.query.get_or_404(id)



    if request.method == "POST":


        image.caption = request.form["caption"]


        db.session.commit()



        return redirect("/dashboard")



    return render_template(

        "edit_image.html",

        image=image

    )








# -------------------------
# DELETE IMAGE
# -------------------------


@app.route(
    "/delete-image/<int:id>"
)

def delete_image(id):


    if not session.get("admin"):

        return redirect("/login")



    image = Image.query.get_or_404(id)



    db.session.delete(image)


    db.session.commit()



    return redirect("/dashboard")









# -------------------------
# VAULT
# -------------------------


@app.route("/vault")

def vault():


    if not session.get("admin"):

        return redirect("/login")



    return render_template(
        "vault.html"
    )








# -------------------------
# START
# -------------------------


if __name__ == "__main__":


    with app.app_context():

        db.create_all()



    app.run(
        debug=True
    )