from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

GAS_URL = "https://script.google.com/macros/s/AKfycbz-tgKm6cIldXu4IWsDcQtZHj_222iaGgkidNEriRZ3zE6S5gKaNIhR8foSerIVERyR/exec"


@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():
    try:
        data = request.form.to_dict()

        r = requests.post(GAS_URL, data=data, timeout=20)

        return jsonify({
            "status": "ok",
            "received": data,
            "gas": r.text
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
