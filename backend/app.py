from flask import Flask, jsonify, request, send_from_directory
from system_monitor import get_system_stats
from process_handler import get_all_processes, kill_process
import os
import psutil

# Initialize Flask App and set static folder to 'frontend'
app = Flask(__name__, static_folder='../frontend')

# Warm up the CPU monitor so the first call isn't 0.0
psutil.cpu_percent(interval=0.1)
# Warm up process CPU limits
for proc in psutil.process_iter():
    try:
        proc.cpu_percent(interval=None)
    except:
        pass

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/system')
def api_system():
    return jsonify(get_system_stats())

@app.route('/api/processes')
def api_processes():
    return jsonify(get_all_processes())

@app.route('/api/kill/<int:pid>', methods=['POST'])
def api_kill(pid):
    result = kill_process(pid)
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

if __name__ == '__main__':
    # Host on localhost only for security
    print("Starting Process Dashboard Backend...")
    app.run(host='127.0.0.1', port=5000, debug=False)
