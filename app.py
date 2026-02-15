from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GAS_URL = "https://script.google.com/macros/s/AKfycbyMk1pz25XRX9r9fifxOnDNVmp-CO_bsU5mkQ6jyumL4gX5iUOCJVi_pKr-zpXOwLuI/exec"

@app.route("/lead", methods=["POST"])
def capture_lead():
    try:
        data = request.form.to_dict()

        r = requests.post(GAS_URL, data=data, timeout=10)

        if r.status_code == 200:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "gas_error", "body": r.text}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Lead Relay Running", 200
