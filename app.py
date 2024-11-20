from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from flask_migrate import Migrate
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# OAuth setup
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google_login_callback"
)
app.register_blueprint(google_bp, url_prefix="/login")


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    social_login_provider = db.Column(db.String(50))
    profile_picture = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    content = db.Column(db.Text, nullable=False)
    meta_info = db.Column(db.JSON, nullable=True)  # Renamed from 'metadata'
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class PromptLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    generated_output = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Routes

@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route("/google_login_callback")
def google_login_callback():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            profile_picture=user_info["picture"],
            social_login_provider="google"
        )
        db.session.add(user)
        db.session.commit()
    session["user_id"] = user.id
    return redirect(url_for("home"))


@app.route("/scrape", methods=["POST"])
def scrape():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401
    user_id = session["user_id"]
    url = request.json.get("url")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        metadata = {
            "title": soup.title.string if soup.title else "No title",
            "description": soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "No description"
        }
        content = soup.get_text()
        scraped_data = ScrapedData(
            url=url, content=content, metadata=metadata, created_by_user_id=user_id
        )
        db.session.add(scraped_data)
        db.session.commit()
        return jsonify({"message": "Data scraped successfully", "metadata": metadata})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_prompt", methods=["POST"])
def generate_prompt():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401
    user_id = session["user_id"]
    data = request.json
    prompt = data.get("prompt")
    try:
        llm = OpenAI(model_name="text-davinci-003")
        response = llm(prompt)
        tokens_used = len(response.split())  # Approximate token count
        prompt_log = PromptLog(
            prompt_text=prompt,
            generated_output=response,
            tokens_used=tokens_used,
            created_by_user_id=user_id
        )
        db.session.add(prompt_log)
        db.session.commit()
        return jsonify({"response": response, "tokens_used": tokens_used})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))
    user_id = session["user_id"]
    scraped_data = ScrapedData.query.filter_by(created_by_user_id=user_id).all()
    prompt_logs = PromptLog.query.filter_by(created_by_user_id=user_id).all()
    return render_template("dashboard.html", scraped_data=scraped_data, prompt_logs=prompt_logs)


# Templates
@app.route("/static/dashboard.html")
def dashboard_template():
    return '''
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
<h1>Dashboard</h1>
<h2>Scraped Data</h2>
<ul>{% for data in scraped_data %}
    <li>{{ data.url }} - {{ data.metadata.title }}</li>
{% endfor %}</ul>
<h2>Prompts</h2>
<ul>{% for log in prompt_logs %}
    <li>{{ log.prompt_text }} - {{ log.generated_output }}</li>
{% endfor %}</ul>
</body>
</html>
'''


if __name__ == "__main__":
    app.run(debug=True)
