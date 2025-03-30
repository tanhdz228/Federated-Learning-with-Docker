from flask import Flask, jsonify, request
from model import initialize_model, aggregate_update
import numpy as np
from threading import Lock

app = Flask(__name__)
global_model = initialize_model()
client_updates = []
lock = Lock()  # Thread lock for synchronization

@app.route('/model', methods=['GET'])
def get_model():
    return jsonify({"model": global_model.tolist()})

@app.route('/update', methods=['POST'])
def receive_update():
    try:
        data = request.json
        if not data or "model" not in data:
            return jsonify({"error": "Missing 'model' in request"}), 400
        
        update = np.array(data["model"], dtype=np.float32)
        
        # Thread-safe append
        with lock:
            client_updates.append(update)
            if len(client_updates) == 2:
                global_model[:] = aggregate_update(client_updates)
                client_updates.clear()
                print(f"[Server] New global model: {global_model}", flush=True)  # Force log output
        
        return jsonify({"status": "Update received"})
    
    except Exception as e:
        print(f"[Server Error] {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)