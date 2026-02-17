from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

GAS_URL = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"


@app.route("/", methods=["GET", "HEAD"])
def home():
    return "Lead relay running", 200


@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():
    try:
        # accept both query + form
        data = request.form.to_dict()
        if not data:
            data = request.args.to_dict()

        print("RECEIVED FROM CHATLNG:", data)

        r = requests.post(GAS_URL, data=data, timeout=15)

        print("GAS STATUS:", r.status_code)
        print("GAS RESPONSE:", r.text)

        return jsonify({
            "status": "success",
            "gas_status": r.status_code,
            "gas_response": r.text,
            "received": data
        }), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
