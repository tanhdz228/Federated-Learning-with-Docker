from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)
global_model = np.zeros(5)  
client_updates = []

@app.route('/model', methods=['GET'])
def get_model():
    return jsonify({'model': global_model.tolist()})

@app.route('/update', methods=['POST'])
def receive_update():
    update = np.array(request.json['model'])
    client_updates.append(update)
    
    if len(client_updates) == 3:  
        global_model[:] = np.mean(client_updates, axis=0)
        client_updates.clear()
        print(f"[Server] New global model: {global_model}", flush=True)
        return jsonify({'status': 'Model aggregated'})
    return jsonify({'status': 'Update received'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)