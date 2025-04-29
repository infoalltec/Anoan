from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-4-maverick:free"

@app.route("/generate", methods=["POST"])
def generate_headlines():
    data = request.get_json()
    keyword = data.get("keyword", "").strip()

    if not keyword:
        return jsonify({"error": "يرجى إدخال كلمة مفتاحية"}), 400

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""اكتب 5 عناوين عربية جذابة ومحسّنة لمحركات البحث حول: {keyword}.
استخدم أساليب احترافية مثل النقطتين (:) أو الشرطات (-) لتقسيم العنوان.
إذا أمكن، استخدم أرقامًا في العنوان لجذب الانتباه.
اجعل العناوين قصيرة، واضحة، فريدة، ومصممة لزيادة معدل النقرات (CTR).
تجنب الرموز غير الضرورية أو التعداد داخل العنوان."""
                    }
                ]
            }
        )
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        titles = [line.strip(" -").strip() for line in content.split("\n") if line.strip()]
        return jsonify({"titles": titles[:5]})
    except Exception as e:
        return jsonify({"error": "فشل الاتصال بالخادم أو استجابة غير صالحة", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
