from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Allow all origins

usage_data = []   # Replace with DB for production!
user_goals = {}

@app.route('/api/upload_usage', methods=['POST'])
def upload_usage():
    sessions = request.json
    if not isinstance(sessions, list):
        return jsonify({'error': 'Expected a list'}), 400
    usage_data.extend(sessions)
    return jsonify({'success': True})

@app.route('/api/set_goals', methods=['POST'])
def set_goals():
    user_goals.update(request.json)
    return jsonify({'success': True, 'goals': user_goals})

@app.route('/api/analytics/today', methods=['GET'])
def analytics_today():
    today = datetime.now().date()
    site_minutes = defaultdict(float)
    for entry in usage_data:
        start_dt = datetime.fromisoformat(entry['start'])
        end_dt = datetime.fromisoformat(entry['end'])
        if start_dt.date() == today:
            minutes = (end_dt - start_dt).total_seconds() / 60
            site_minutes[entry['site']] += minutes
    return jsonify({'site_minutes': site_minutes, 'goals': user_goals})

@app.route('/api/analytics/trends', methods=['GET'])
def analytics_trends():
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    trends = defaultdict(lambda: defaultdict(float))
    for entry in usage_data:
        start_dt = datetime.fromisoformat(entry['start'])
        end_dt = datetime.fromisoformat(entry['end'])
        if week_ago <= start_dt <= now:
            day = start_dt.strftime('%Y-%m-%d')
            minutes = (end_dt - start_dt).total_seconds() / 60
            trends[day][entry['site']] += minutes
    return jsonify(trends)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
