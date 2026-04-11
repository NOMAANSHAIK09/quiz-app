from flask import Flask, json, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.security import generate_password_hash
# login system
from werkzeug.security import check_password_hash
from datetime import datetime
from flask import session
import re
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
load_dotenv()

API_KEYS = [
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
    os.getenv("API_KEY_4"),
    os.getenv("API_KEY_5"),
]

# 🔥 FALLBACK FUNCTION
def generate_quiz_with_fallback(payload):
    url = "https://openrouter.ai/api/v1/chat/completions"

    for key in API_KEYS:
        if not key:
            continue

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                print(f"✅ Working KEY: {key[:10]}...")
                return response.json()
            else:
                print(f"❌ Failed KEY: {key[:10]} | Status: {response.status_code}")

        except Exception as e:
            print(f"⚠️ Error KEY {key[:10]}: {e}")

    return None


app = Flask(__name__)

app.config['SECRET_KEY'] = "09012007"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ADMIN_EMAIL = os.getenv("ADMIN_G")

ADMIN_PASSWORD = os.getenv("ADMIN_PASS")

db = SQLAlchemy(app)

# ---------------- MODEL ---------------- it create a table if not exixt 
class user_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(200))
    
class user_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    topic = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def home():
    outputs=0
    if 'username' in session:
        print(session['username'])
        return render_template("index.html", outputs=session['username'])
    return render_template("index.html", outputs=None)

#start quiz route it get data from form and send to open router ai and get response in json format and pass to quiz page
@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    questions={}
    if request.method == "POST":
        
        quiz_topic = request.form.get("topic")
        difficulty = request.form.get("difficulty")

        system_prompt = f"""
        Generate 10 quiz questions on '{quiz_topic}' with '{difficulty}' difficulty.
        
        STRICT RULES:
        - Return ONLY JSON array
        - Do NOT add explanation
        - Do NOT use ```json
        - Do NOT write any text before or after
        
        Return ONLY valid JSON:
        [
          {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "..."
          }}
        ]
        and and 
        IMPORTANT:
            - "answer" must be EXACT same as one of the options
            - Do NOT use A/B/C/D
            - Use full text answer

            Example:
            "options": ["Snake", "Language", "Game", "Car"],
            "answer": "Language"
        """

        url = "https://openrouter.ai/api/v1/chat/completions"

        # headers = {
        #     "Authorization": f"Bearer {key}",
        #     "Content-type": "application/json"
        # }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate quiz"}
            ],
            "temperature": 0.7,
        }
        quiz_data = generate_quiz_with_fallback(payload)

        if quiz_data:
            raw_output = quiz_data['choices'][0]['message']['content']
            raw_output = raw_output.strip()

            if raw_output.startswith("```"):
                raw_output = raw_output.replace("```json", "").replace("```", "").strip()

            match = re.search(r"\[.*\]", raw_output, re.DOTALL)

            if not match:
                return render_template("start_quiz.html", error="⚠️ Failed to extract quiz data")

            try:
                questions = json.loads(match.group(0))
                session['answers'] = [q['answer'] for q in questions]
                session["questions"] = questions
                session["topic"] = quiz_topic
                session["difficulty"] = difficulty
                
                return render_template("quiz.html", questions=questions)

            except Exception as e:
                print("JSON ERROR:", e)
                return render_template("start_quiz.html", error="⚠️ Error parsing quiz")

        else:
            return render_template("start_quiz.html", error="⚠️ All API keys failed")

    return render_template("start_quiz.html")

    #     response = requests.post(url, headers=headers, json=payload)

    #     if response.status_code == 200:
    #         quiz_data = response.json()
    #         raw_output = quiz_data['choices'][0]['message']['content']
    #         raw_output = raw_output.strip()

    #         if raw_output.startswith("```"):
    #             raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    #         # print("RAW OUTPUT:", raw_output)

    #         # Extract JSON
    #         match = re.search(r"\[.*\]", raw_output, re.DOTALL)

    #         if not match:
    #             return render_template("start_quiz.html", error="⚠️ Failed to extract quiz data")

    #         try:
    #             questions = json.loads(match.group(0))
    #             session['answers'] = [q['answer'] for q in questions]
    #             session["questions"] = questions
    #             session["topic"] = quiz_topic
    #             session["difficulty"] = difficulty
                
    #             return render_template("quiz.html", questions=questions)

    #         except Exception as e:
    #             print("JSON ERROR:", e)
    #             return render_template("start_quiz.html", error="⚠️ Error parsing quiz")

    #     else:
    #         print("API ERROR:", response.status_code)
    #         return render_template("start_quiz.html", error="⚠️ API request failed")

    # return render_template("start_quiz.html")


# ---------------- ROUTE ---------------- first signup logic if method is post \
#the it get data from form page and stor in data base hashed password used for passsword securaty 
@app.route("/signup", methods=("GET", "POST"))
def signup_page():
    if request.method == "POST": 
        #extracting form data
        user_name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # hash password
        hashed_password = generate_password_hash(password)
        # it collect data and store in database
        user = user_info(
            user_name=user_name,
            email=email,
            password=hashed_password
        )
        #add and comit to data base 
        db.session.add(user)
        db.session.commit()
        #create a popo up msg  
        flash("Account created successfully!", "success")
        #restart the signup page
        return redirect(url_for("home"))

    return render_template("signup.html")



# @app.route("/login", methods=["GET", "POST"])
# def login_page():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]

#         user = user_info.query.filter_by(email=email).first()

#         if user and check_password_hash(user.password, password):
#             session["user_id"] = user.id
#             session["username"] = user.user_name
#             flash("Login successful!", "success")
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid email or password", "danger")

#     return render_template("login.html")
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # 🔥 ADMIN LOGIN CHECK (FIRST)
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Admin login successful!", "success")
            return redirect(url_for("admin_dashboard"))

        # 👤 NORMAL USER LOGIN
        user = user_info.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.user_name
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

 



@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("login_page"))


# @app.route("/result", methods=["POST"])
# def result():
#     questions = session.get("questions", [])
#     correct_answers = session.get("answers", [])
#     score = 0
#     user_answers = []   # 🔥 ADD THIS

#     for i, correct in enumerate(correct_answers, start=1):
#         user_ans = request.form.get(f"q{i}")
#         user_answers.append(user_ans)   # 🔥 STORE USER ANSWER

#         if user_ans and correct:
#             if user_ans.strip().lower() == correct.strip().lower():
#                 score += 1

#         # print(f"Q{i} -> User: {user_ans}, Correct: {correct}")

#     return render_template(
#         "result.html",
#         score=score,
#         total=len(correct_answers),
#         questions=questions,
#         correct_answers=correct_answers,
#         user_answers=user_answers   # 🔥 PASS THIS
#     )
@app.route("/result", methods=["POST"])
def result():
    questions = session.get("questions", [])
    correct_answers = session.get("answers", [])

    if not questions or not correct_answers:
        flash("Session expired! Please take quiz again.", "danger")
        return redirect(url_for("start_quiz"))

    score = 0
    user_answers = []

    for i, correct in enumerate(correct_answers, start=1):
        user_ans = request.form.get(f"q{i}")
        user_answers.append(user_ans)

        # if user_ans and correct:
    
        #     user_letter = user_ans.strip()[0].upper()
        #     correct_letter = correct.strip()[0].upper()

        #     if user_letter == correct_letter:
        #         score += 1
        if user_ans and correct:
    # Remove "A. " or "B. " from user answer
            clean_user = user_ans.split(". ", 1)[-1].strip().lower()
            clean_correct = correct.strip().lower()

            if clean_user == clean_correct:
                score += 1
    print(f"FINAL SCORE: {score} / {len(correct_answers)}")
                
    if "user_id" in session:
        new_score = user_scores(
            user_id=session["user_id"],
            topic=session.get("topic"),
            difficulty=session.get("difficulty"),
            score=score
        )
        db.session.add(new_score)
        db.session.commit()

    return render_template(
        "result.html",
        score=score,
        total=len(correct_answers),
        questions=questions,
        correct_answers=correct_answers,
        user_answers=user_answers
    )
    
@app.route("/history")
def history():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login_page"))

    user_id = session["user_id"]

    # 🔥 Get only this user's scores
    scores = user_scores.query.filter_by(user_id=user_id).all()

    return render_template("history.html", scores=scores)
        
        
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        flash("Access denied!", "danger")
        return redirect(url_for("login_page"))

    total_users = user_info.query.count()
    total_quizzes = user_scores.query.count()

    # 🏆 TOP SCORES
    top_scores = db.session.query(
        user_info.user_name,
        user_scores.score,
        user_scores.topic
    ).join(user_info).order_by(user_scores.score.desc()).limit(5).all()

    # 📅 RECENT ACTIVITY
    recent = db.session.query(
        user_info.user_name,
        user_scores.topic,
        user_scores.score,
        user_scores.date
    ).join(user_info).order_by(user_scores.date.desc()).limit(5).all()

    # 📋 ALL DATA
    all_scores = db.session.query(
        user_info.user_name,
        user_scores.topic,
        user_scores.difficulty,
        user_scores.score,
        user_scores.date
    ).join(user_info).all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_quizzes=total_quizzes,
        top_scores=top_scores,
        recent=recent,
        all_scores=all_scores
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

