from flask import Flask, request, jsonify
import requests
import threading
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

GAS_URL = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"


def send_to_gas(data):
    try:
        requests.post(GAS_URL, data=data, timeout=20)
    except:
        pass


@app.route("/")
def home():
    return "Lead relay running", 200


@app.route("/lead", methods=["POST"])
def capture_lead():
    data = request.form.to_dict()

    threading.Thread(target=send_to_gas, args=(data,)).start()

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
