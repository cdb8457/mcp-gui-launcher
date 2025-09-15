function startService(serviceName) {
    fetch(`/start/${serviceName}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}

function stopService(serviceName) {
    fetch(`/stop/${serviceName}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}

function setApiKey() {
    const apiKey = document.getElementById('api-key').value;
    fetch('/set_api_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `api_key=${encodeURIComponent(apiKey)}`
    })
    .then(response => response.json())
    .then(data => {
        alert('API Key set successfully');
    })
    .catch(error => console.error('Error:', error));
}