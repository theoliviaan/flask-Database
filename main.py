import os

from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, "users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(25), nullable=False)

# Representation of your data
    def __repr__(self):
        return f"User {self.username}"


@app.route('/')
def home():
    users = User.query.all()

    context = {
        "users": users
    }
    return render_template("index.html", **context)


@app.route('/users', methods=['POST'])
def create_user():
    user_username = request.form.get('username')
    user_email = request.form.get('email')
    user_age = request.form.get('age')
    user_gender = request.form.get('gender')

    new_user = User(username=user_username, email=user_email, age=user_age, gender=user_gender)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    user_to_update = User.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.username = request.form.get("username")
        user_to_update.email = request.form.get("email")
        user_to_update.age = request.form.get("age")
        user_to_update.gender = request.form.get("gender")

        db.session.commit()

        return redirect(url_for('home'))

    context = {
        "user": user_to_update
    }

    return render_template("update.html", **context)

@app.route("/delete/<int:id>",methods=['GET'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect(url_for('home'))



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)