from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Health check
@app.route("/")
def home():
    return "Lead relay running", 200


# Lead endpoint (Chatling calls this)
@app.route("/lead", methods=["POST"])
def capture_lead():
    try:
        data = request.form.to_dict()

        gas_url = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"

        response = requests.post(gas_url, data=data, timeout=15)

        if response.status_code == 200:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "gas": response.text}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run()

