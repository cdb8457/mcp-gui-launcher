from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

CONFIG_FILE = '/app/config/config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"api_key": "", "other_settings": {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

@app.route('/')
def index():
    # Get list of services
    services = [
        {'name': 'mcp-server-free', 'status': 'stopped', 'type': 'free'},
        {'name': 'mcp-server-paid', 'status': 'stopped', 'type': 'paid'}
    ]
    # In real implementation, check actual status
    return render_template('index.html', services=services)

@app.route('/start/<service_name>', methods=['POST'])
def start_service(service_name):
    try:
        profile = 'mcp-free' if 'free' in service_name else 'mcp-paid'
        result = subprocess.run(f'docker-compose --profile {profile} up -d {service_name}', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': f'{service_name} started'})
        else:
            return jsonify({'status': 'error', 'message': result.stderr})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop/<service_name>', methods=['POST'])
def stop_service(service_name):
    try:
        result = subprocess.run(f'docker-compose stop {service_name}', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': f'{service_name} stopped'})
        else:
            return jsonify({'status': 'error', 'message': result.stderr})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    config = load_config()
    config['api_key'] = request.form.get('api_key', '')
    save_config(config)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)