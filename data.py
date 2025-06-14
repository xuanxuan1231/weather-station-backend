import os
import requests
import json

UPSTASH_REDIS_REST_URL = os.environ.get("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
    "Content-Type": "application/json"
}

REDIS_KEY = "weather_data"

def get_redis_data():
    url = f"{UPSTASH_REDIS_REST_URL}/get/{REDIS_KEY}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        val = resp.json().get('result')
        if val:
            return json.loads(val)
    # 默认结构
    return {"temp": [], "humidity": [], "pressure": [], "pm2_5": []}

def set_redis_data(data):
    url = f"{UPSTASH_REDIS_REST_URL}/set/{REDIS_KEY}"
    payload = json.dumps(data)
    resp = requests.post(url, headers=HEADERS, data=payload)
    return resp.status_code == 200

def add_temp(temp, time):
    data = get_redis_data()
    data["temp"].append({"temp": temp, "time": time})
    set_redis_data(data)

def get_temp():
    try:
        data = get_redis_data()
        return data["temp"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增湿度相关方法
def add_humidity(humidity, time):
    data = get_redis_data()
    data["humidity"].append({"humidity": humidity, "time": time})
    set_redis_data(data)

def get_humidity():
    try:
        data = get_redis_data()
        return data["humidity"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增气压相关方法
def add_pressure(pressure, time):
    data = get_redis_data()
    data["pressure"].append({"pressure": pressure, "time": time})
    set_redis_data(data)

def get_pressure():
    try:
        data = get_redis_data()
        return data["pressure"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增pm2.5相关方法
def add_pm2_5(pm2_5, time):
    data = get_redis_data()
    data["pm2_5"].append({"pm2_5": pm2_5, "time": time})
    set_redis_data(data)

def get_pm2_5():
    try:
        data = get_redis_data()
        return data["pm2_5"][-1]
    except Exception as e:
        return {"error": str(e)}