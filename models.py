from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_chat_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: API key not found. Please set the GEMINI_API_KEY environment variable."
    
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use the correct model name
        response = model.generate_content(
            f"As Bennett University chatbot, answer only about university matters: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"