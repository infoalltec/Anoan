from flask import Flask, request, jsonify import requests import os

app = Flask(name)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/generate", methods=["POST"]) def generate(): data = request.get_json() keyword = data.get("keyword", "").strip()

if not keyword:
    return jsonify({"error": "يرجى إدخال كلمة مفتاحية."}), 400

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-blog-url.com",
    "X-Title": "Headline Generator"
}

body = {
    "model": "meta-llama/llama-4-maverick:free",
    "messages": [
        {
            "role": "user",
            "content": f"اكتب 5 عناوين مقالات عربية فقط (بدون أرقام) عن \"{keyword}\" باستخدام النقطتين كفاصل"
        }
    ]
}

try:
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return jsonify({"titles": content})
except Exception as e:
    return jsonify({"error": str(e)}), 500

if name == "main": app.run(host="0.0.0.0", port=5000)

