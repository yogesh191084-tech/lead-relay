from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

GAS_URL = "https://docs.google.com/spreadsheets/d/11na5_qyFEXxyxU7R0wum67NKPSZ5l0g7-b6hZ0Uqq0o/edit?gid=0#gid=0"


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
