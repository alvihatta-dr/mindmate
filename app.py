import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import markdown 

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    import sys
    print("API key tidak ditemukan. Setel GEMINI_API_KEY sebagai environment variable atau di .env")
    sys.exit(1)

genai.configure(api_key=api_key)

# Konfigurasi Gemini client
os.environ["GEMINI_API_KEY"] = api_key
client = genai.Client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_input = request.json.get("user_input")
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/konsultasi", methods=["POST"])
def konsultasi():
    data = request.get_json()
    user_input = data.get("pesan", "")
    template = (
      "Tolong jawab dalam format markdown terstruktur. "
      "Gunakan **bold**, *italic*, list numerik dan bullet. "
      "Contohnya:\n\n"
      "## I. SELF-CARE\n"
      "- **Tidur cukup**\n"
      "- *Hindari gadget sebelum tidur*\n\n"
      "## II. STRES MANAGEMENT\n"
      "- Identifikasi stres\n- Curhat\n\n"
      f"Pertanyaan:\n{user_input}"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=template
    )
    md = response.text
    html = markdown.markdown(md)
    return jsonify({'jawaban': html})


if __name__ == "__main__":
    app.run(debug=True)
