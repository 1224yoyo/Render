#flask.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # 1. 匯入它
import redis
import json

app = Flask(__name__)

# 直接貼上你的連線字串
url = "rediss://default:AZrhAAIncDFkYjBhY2ZhMmE5NTY0ODdhOTJhOGNkYTliNDRiMjIxOXAxMzk2NDk@guiding-weevil-39649.upstash.io:6379"

# 連線 (rediss 代表使用 TLS 加密)
r = redis.from_url(url, decode_responses=True)

CORS(app)

@app.route("/login", methods=["POST"])
def read_user():
    name = request.form.get("username")   # 🔥 改這裡
    password = request.form.get("password")

    js = {"data": None}

    data = r.json().get("user_json", f"$.{name}")

    if data != []:
        data = data[0]
        if password == data["password"]:
            js["data"] = f'name: {data["name"]} password: {data["password"]}'
        else:
            js["data"] = "password no True"
    else:
        js["data"] = "no find User"

    return jsonify(js)

if __name__ == "__main__":
    app.run(debug=True)
#flask.py
