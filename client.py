from flask import Flask, jsonify
import requests
import numpy as np

app = Flask(__name__)
CENTRAL_SERVER_URL = 'http://central-server:5000' 

@app.route('/train', methods=['GET'])
def train():
    #fetch global model
    response = requests.get(f'{CENTRAL_SERVER_URL}/model')
    global_model = np.array(response.json()['model'])
    
    #simulate local training (add random noise)
    local_update = global_model + np.random.normal(0, 0.1, size=global_model.shape)
    
    #send update to server
    requests.post(
        f'{CENTRAL_SERVER_URL}/update',
        json={'model': local_update.tolist()}
    )
    print(f"[Client] Sent update: {local_update}")
    return jsonify({'status': 'Update sent'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)