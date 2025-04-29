from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-4-maverick:free"

@app.route("/")
def index():
    return "OpenRouter Flask API is running."

@app.route("/generate", methods=["POST"])
def generate_headlines():
    data = request.get_json()
    keyword = data.get("keyword", "").strip()

    if not keyword:
        return jsonify({"error": "يرجى إدخال كلمة مفتاحية"}), 400

    try:
        prompt = (
            f"أنت مساعد محترف في كتابة المحتوى، مهمتك هي توليد 5 عناوين "
            f"لمقالات عربية جذابة ومقنعة وجاهزة للنشر على مدونة. "
            f"يجب أن تستخدم أفضل ممارسات تحسين محركات البحث (SEO) مثل تضمين الكلمة المفتاحية بشكل طبيعي، "
            f"وصياغة العنوان بطريقة تشجع على النقر، دون استخدام رموز أو ترقيم. "
            f"الكلمة المفتاحية هي: {keyword}. لا تكرر الكلمة المفتاحية أكثر من مرة في العنوان الواحد، واجعل كل عنوان فريدًا."
        )

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://anoan.onrender.com",
                "X-Title": "Blogger AI Headlines"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        titles = [line.strip(" -•").strip() for line in content.split("\n") if len(line.strip()) > 5]
        return jsonify({"titles": titles[:5]})
    except Exception as e:
        return jsonify({"error": "فشل الاتصال بالخادم أو استجابة غير صالحة", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
