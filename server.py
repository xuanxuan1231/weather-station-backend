import datetime

import flask
from flask import Flask, request, jsonify
from flask import make_response

import data

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/temp", methods=["POST"])
def add_temp():
    temp = request.json["temp"]
    time = datetime.datetime.now().isoformat()
    if not temp:
        return jsonify({"status": 1, "error": "temp is required"}), 400
    data.add_temp(temp, time)
    return jsonify({"status": 0, "temp": temp, "time": time}), 200


@app.route("/api/temp", methods=["GET"])
def get_temp():
    temp_data = data.get_temp()
    if "error" in temp_data:
        return jsonify({"status": 1, "error": temp_data["error"]}), 500
    return jsonify(
        {"status": 0, "temp": temp_data["temp"], "time": temp_data["time"]}
    ), 200


# 新增湿度接口
@app.route("/api/humidity", methods=["POST"])
def add_humidity():
    humidity = request.json["humidity"]
    time = datetime.datetime.now().isoformat()
    if not humidity:
        return jsonify({"status": 1, "error": "humidity is required"}), 400
    data.add_humidity(humidity, time)
    return jsonify({"status": 0, "humidity": humidity, "time": time}), 200


@app.route("/api/humidity", methods=["GET"])
def get_humidity():
    humidity_data = data.get_humidity()
    if "error" in humidity_data:
        return jsonify({"status": 1, "error": humidity_data["error"]}), 500
    return jsonify(
        {
            "status": 0,
            "humidity": humidity_data["humidity"],
            "time": humidity_data["time"],
        }
    ), 200


# 新增气压接口
@app.route("/api/pressure", methods=["POST"])
def add_pressure():
    pressure = request.json["pressure"]
    time = datetime.datetime.now().isoformat()
    if not pressure:
        return jsonify({"status": 1, "error": "pressure is required"}), 400
    data.add_pressure(pressure, time)
    return jsonify({"status": 0, "pressure": pressure, "time": time}), 200


@app.route("/api/pressure", methods=["GET"])
def get_pressure():
    pressure_data = data.get_pressure()
    if "error" in pressure_data:
        return jsonify({"status": 1, "error": pressure_data["error"]}), 500, 
    return jsonify(
        {
            "status": 0,
            "pressure": pressure_data["pressure"],
            "time": pressure_data["time"],
        }
    ), 200


# 新增pm2.5接口
@app.route("/api/pm2_5", methods=["POST"])
def add_pm2_5():
    pm2_5 = request.json["pm2_5"]
    time = datetime.datetime.now().isoformat()
    if not pm2_5:
        return jsonify({"status": 1, "error": "pm2_5 is required"}), 400
    data.add_pm2_5(pm2_5, time)
    return jsonify({"status": 0, "pm2_5": pm2_5, "time": time}), 200


@app.route("/api/pm2_5", methods=["GET"])
def get_pm2_5():
    pm2_5_data = data.get_pm2_5()
    if "error" in pm2_5_data:
        return jsonify({"status": 1, "error": pm2_5_data["error"]}), 500
    return jsonify(
        {"status": 0, "pm2_5": pm2_5_data["pm2_5"], "time": pm2_5_data["time"]}
    ), 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://wt.gemen.pp.ua')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
