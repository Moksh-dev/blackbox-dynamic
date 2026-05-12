import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
cloudinary.config(
    cloud_name="dnvmvfr4w",
    api_key="992199383868877",
    api_secret="f54uwtrgJztfHQnSfewHyDgdmHM"
)
app.secret_key = "blackbox-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blackbox.db'

db = SQLAlchemy(app)

class Thought(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text)

    created = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text)

    approved = db.Column(db.Boolean, default=False)

class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    image_url = db.Column(db.Text)

    caption = db.Column(db.Text)

@app.route('/')
def home():

    thoughts = Thought.query.order_by(
        Thought.created.desc()).all()

    images = Image.query.all()

    return render_template(
        'index.html',
        thoughts=thoughts,
        images=images
    )
@app.route('/submit', methods=['GET', 'POST'])
def submit():

    if request.method == 'POST':

        content = request.form['content']

        new_submission = Submission(
            content=content
        )

        db.session.add(new_submission)

        db.session.commit()

        return redirect('/')

    return render_template('submit.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        password = request.form['password']

        if password == "mokshblackbox":

            session['admin'] = True

            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if not session.get('admin'):

        return redirect('/login')

    thoughts = Thought.query.all()

    submissions = Submission.query.all()

    return render_template(
        'dashboard.html',
        thoughts=thoughts,
        submissions=submissions
    )

@app.route('/add-thought', methods=['POST'])
def add_thought():

    content = request.form['content']

    new_thought = Thought(content=content)

    db.session.add(new_thought)

    db.session.commit()

    return redirect('/dashboard')

@app.route('/upload-image', methods=['POST'])
def upload_image():

    if not session.get('admin'):

        return redirect('/login')

    file = request.files['image']

    caption = request.form['caption']

    result = cloudinary.uploader.upload(file)

    image_url = result['secure_url']

    new_image = Image(
        image_url=image_url,
        caption=caption
    )

    db.session.add(new_image)

    db.session.commit()

    return redirect('/dashboard')

@app.route('/approve/<int:id>')
def approve(id):

    submission = Submission.query.get(id)

    new_thought = Thought(
        content=submission.content
    )

    db.session.add(new_thought)

    db.session.delete(submission)

    db.session.commit()

    return redirect('/dashboard')

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)