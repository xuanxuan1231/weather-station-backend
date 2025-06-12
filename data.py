import json

def add_temp(temp, time):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"temp": [], "humidity": [], "pressure": [], "pm2_5": []}
    
    data["temp"].append({
        "temp": temp, 
        "time": time
    })
    with open("data.json", "w") as file:
        json.dump(data, file)

def get_temp():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data["temp"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增湿度相关方法
def add_humidity(humidity, time):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"temp": [], "humidity": [], "pressure": [], "pm2_5": []}
    data["humidity"].append({
        "humidity": humidity,
        "time": time
    })
    with open("data.json", "w") as file:
        json.dump(data, file)

def get_humidity():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data["humidity"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增气压相关方法
def add_pressure(pressure, time):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"temp": [], "humidity": [], "pressure": [], "pm2_5": []}
    data["pressure"].append({
        "pressure": pressure,
        "time": time
    })
    with open("data.json", "w") as file:
        json.dump(data, file)

def get_pressure():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data["pressure"][-1]
    except Exception as e:
        return {"error": str(e)}

# 新增pm2.5相关方法
def add_pm2_5(pm2_5, time):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"temp": [], "humidity": [], "pressure": [], "pm2_5": []}
    data["pm2_5"].append({
        "pm2_5": pm2_5,
        "time": time
    })
    with open("data.json", "w") as file:
        json.dump(data, file)

def get_pm2_5():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data["pm2_5"][-1]
    except Exception as e:
        return {"error": str(e)}