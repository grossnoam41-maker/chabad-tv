from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"
DEFAULT_DATA = {
    "bulletin_message": "ברוכים הבאים לבית חב\"ד! שבת שלום ומבורכת.",
    "shul_hours": "שחרית: 08:30\nמנחה וערבית: 15 דקות לפני השקיעה",
    "kiddush_info": "הקידוש השבוע נתרם להצלחת משפחת הקהילה.",
    "contact_info": "שליח חב\"ד: הרב לוי\nטלפון: 050-1234567"
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=4)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/update-chabad-panel-98725', methods=['POST'])
def update_data():
    req_data = request.json
    if not req_data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    current_data = load_data()
    current_data["bulletin_message"] = req_data.get("bulletin_message", current_data["bulletin_message"])
    current_data["shul_hours"] = req_data.get("shul_hours", current_data["shul_hours"])
    current_data["kiddush_info"] = req_data.get("kiddush_info", current_data["kiddush_info"])
    current_data["contact_info"] = req_data.get("contact_info", current_data["contact_info"])
    
    save_data(current_data)
    return jsonify({"status": "success", "message": "Data updated successfully"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
