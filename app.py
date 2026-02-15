from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

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

    # async send so Chatling gets instant response
    threading.Thread(target=send_to_gas, args=(data,)).start()

    return jsonify({"status": "success"}), 200
