from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di environment.")

genai.configure(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/konsultasi', methods=['POST'])
def konsultasi():
    data = request.get_json()
    pesan = data.get('pesan')

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(pesan)

        # Konversi Markdown → HTML
        html_jawaban = markdown.markdown(response.text)
        return jsonify({'jawaban': html_jawaban})
    except Exception as e:
        return jsonify({'jawaban': f"❌ Error: {str(e)}"})
