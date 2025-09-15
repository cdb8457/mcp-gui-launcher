from flask import Flask, render_template, request, jsonify
import docker
import os

app = Flask(__name__)

# Docker client
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

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
        os.system(f'docker-compose --profile {profile} up -d {service_name}')
        return jsonify({'status': 'success', 'message': f'{service_name} started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop/<service_name>', methods=['POST'])
def stop_service(service_name):
    try:
        os.system(f'docker-compose stop {service_name}')
        return jsonify({'status': 'success', 'message': f'{service_name} stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    # Save to config or env
    with open('/app/config/api_key.txt', 'w') as f:
        f.write(api_key)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)