from app.tasks import run_spider

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "running"}), 200

@app.route("/scrape", methods=["POST"])
def start_scrape():
    """ Endpoint for manual scraping """
    data = request.get_json()
    
    if not data or "urls" not in data or "patterns" not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    if not (isinstance(data.get("urls"), list) or isinstance(data.get("urls"), str)) or not (isinstance(data.get("patterns"), dict) or isinstance(data.get("patterns"), list)):
        return jsonify({"error": "Invalid parameter types"}), 400
    
    task = run_spider.delay(data.get("urls"), data.get("patterns"))
    
    return jsonify({
        "task_id": task.id,
        "status": "Task submitted successfully"
    })
