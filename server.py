import os
import datetime

import flask
import requests
from flask import Flask, request, jsonify, render_template, stream_template
from flask import make_response

import data

app = Flask(__name__)

try:
    token = os.environ['TOKEN']
except:
    token = "114514"


@app.route("/")
def home():
    response = requests.post(
        "https://api.github.com/markdown",
        headers={"Content-Type": "application/json",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"},
        json={
            "text": "# 天气数据 API\n"
                    "这是一个天气数据 API。由 Upstash 提供 Redis 数据库服务。\n"
                    "## API 端点\n"
                    "所有的 API 端点同时可以使用 `POST` 和 `GET` 方法。`POST` 方法用于上报数据，`GET` 方法用于获取数据。\n"
                    "| 数据 | 端点 |\n"
                    "| ---- | ---- |\n"
                    "| 温度 | `/api/temp` |\n"
                    "| 湿度 | `/api/humidity` |\n"
                    "| 气压 | `/api/pressure` |\n"
                    "| PM2.5 | `/api/pm2_5` |\n"
                    "## 数据上报\n"
                    "使用 `POST` 方法。携带请求头 `Content-Type: application/json` 和 `Token`。\n"
                    "### 请求体\n"
                    "```json\n"
                    "{\n"
                    "  \"temp\": 25.5,\n"
                    "}\n"
                    "```\n"
                    "`temp` 以实际请求的 API 端点为准。\n"
                    "### 响应体\n"
                    "遇到错误：\n"
                    "```json\n"
                    "{\n"
                    "  \"status\": 1,\n"
                    "  \"error\": \"Invalid token\"\n"
                    "}\n"
                    "```\n"
                    "`error` 以实际错误信息为准。\n"
                    "或，正常时：\n"
                    "```json\n"
                    "{\n"
                    "  \"status\": 0,\n"
                    "  \"temp\": 25.5,\n"
                    "  \"time\": \"2023-10-01T12:00:00\"\n"
                    "}\n"
                    "```\n"
                    "`temp` 以实际请求的 API 端点为准。`25.5` 以实际上报的数据为准。\n"
                    "## 数据获取\n"
                    "使用 `GET` 方法。不需要特别携带请求头。\n"
                    "注意跨域请求。\n"
                    "### 响应体\n"
                    "遇到错误：\n"
                    "```json\n"
                    "{\n"
                    "  \"status\": 1,\n"
                    "  \"error\": \"No data available\"\n"
                    "}\n"
                    "```\n"
                    "`error` 以实际错误信息为准。\n"
                    "或，正常时：\n"
                    "```json\n"
                    "{\n"
                    "  \"status\": 0,\n"
                    "  \"temp\": 25.5,\n"
                    "  \"time\": \"2023-10-01T12:00:00\"\n"
                    "}\n"
                    "```\n"
                    "`temp` 以实际请求的 API 端点为准。`25.5` 以实际存储的数据为准。\n",
            "mode": "gfm",
        })
    if response.status_code == 200:
        return make_response(render_template("main.html", contents=response.text))
    return "Weather API", 200


@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/temp", methods=["POST"])
def add_temp():
    temp = request.json["temp"]
    if request.headers["Token"] != token:
        return jsonify({"status": 1, "error": "Invalid token"}), 401
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
    if request.headers["Token"] != token:
        return jsonify({"status": 1, "error": "Invalid token"}), 401
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


@app.route("/api/pressure", methods=["GET"])
def get_pressure():
    city = "北京"  # 可根据实际需求动态获取
    url = f"https://weatherapi.market.xiaomi.com/wtr-v3/weather/all?latitude=0&longitude=0&locationKey=weathercn:101010100&appKey=weather20151024&sign=zUFJoAR2ZVrDy1vF3D07&isGlobal=false&locale=zh_cn"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return jsonify({"status": 1, "error": "Failed to fetch from Xiaomi Weather"}), 500
        weather = resp.json()
        # 假设返回结构如下，请根据实际API返回结构调整
        pressure = weather["current"]["pressure"]["value"]
        time = weather["current"]["pubTime"]
        if pressure is None:
            return jsonify({"status": 1, "error": "No pressure data from Xiaomi Weather"}), 500
        return jsonify({
            "status": 0,
            "pressure": pressure,
            "time": time
        }), 200
    except Exception as e:
        return jsonify({"status": 1, "error": str(e)}), 500


@app.after_request
def after_request(response):

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
