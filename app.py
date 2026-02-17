from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "Lead relay running", 200


@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():

    # ✅ Ignore browser preflight
    if request.method == "OPTIONS":
        return "", 200

    try:
        # accept both query and form (Chatling sends query)
        data = request.args.to_dict() or request.form.to_dict()

        gas_url = "https://script.google.com/macros/s/AKfycbz-tgKm6cIldXu4IWsDcQtZHj_222iaGgkidNEriRZ3zE6S5gKaNIhR8foSerIVERyR/exec"

        r = requests.post(gas_url, data=data, timeout=15)

        print("RECEIVED:", data)
        print("GAS:", r.status_code, r.text)

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
