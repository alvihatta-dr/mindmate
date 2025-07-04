import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import markdown

# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Validasi API Key
if not api_key:
    raise ValueError("API key tidak ditemukan. Pastikan GEMINI_API_KEY sudah diatur.")

# Konfigurasi Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Inisialisasi Flask
app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt tidak boleh kosong"}), 400

    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
