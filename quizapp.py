from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = "09012007"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class user_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(200))
# ---------------- ROUTE ----------------
@app.route("/signup", methods=("GET", "POST"))
def signup_page():
    if request.method == "POST": 
        user_name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # hash password
        hashed_password = generate_password_hash(password)

        user = user_info(
            user_name=user_name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("signup_page"))

    return render_template("signup.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

