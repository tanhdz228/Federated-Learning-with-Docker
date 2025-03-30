from flask import Flask, jsonify
import requests
import numpy as np

app = Flask(__name__)
SERVER_URL = "http://central-server:5000"

@app.route('/train', methods=['GET'])
def train():
    try:
        response = requests.get(f"{SERVER_URL}/model")
        global_model_list = response.json().get("model")
        print(f"[Client] Fetched model: {global_model_list}")  
        
        if not global_model_list:
            raise ValueError("Empty model received from server")
        
        global_model = np.array(global_model_list, dtype=np.float32)
        local_update = global_model + np.random.normal(0, 0.1, size=global_model.shape)
        
        # Send update to server
        response = requests.post(
            f"{SERVER_URL}/update",
            json={"model": local_update.tolist()}
        )
        print(f"[Client] Server response: {response.text}")  
        
        return jsonify({"status": "Training complete"})
    
    except Exception as e:
        print(f"[Client Error] {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)