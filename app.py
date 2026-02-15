from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Lead relay running", 200


@app.route("/lead", methods=["POST"])
def capture_lead():
    try:
        data = request.form.to_dict()

        gas_url = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"

        r = requests.post(gas_url, data=data, timeout=15)

        return jsonify({
            "status": "success",
            "gas_status": r.status_code
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

