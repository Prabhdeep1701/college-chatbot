from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import authenticate_user, register_user
from models import init_db, get_chat_response
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'bennett-university-chatbot-secret-key'  # Fixed secret key
init_db(app)  # Pass the app instance to init_db

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            session['email'] = email
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if register_user(email, password):
            return redirect(url_for('login'))
        return "Registration failed", 400
    return render_template('login.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        user_input = request.json['message']
        response = get_chat_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)