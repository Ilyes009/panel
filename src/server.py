from flask import Flask, request, jsonify
from flask_cors import CORS
from src.auth.keyauth import api
import hashlib
import sys

app = Flask(__name__)
CORS(app)

def get_checksum():
    md5_hash = hashlib.md5()
    with open(''.join(sys.argv), "rb") as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

keyauthapp = api(
    name="HydraV1",
    ownerid="fV0uvYnrch",
    version="1.0",
    hash_to_check=get_checksum()
)

@app.route('/auth/validate', methods=['POST'])
def validate_key():
    try:
        key = request.json.get('key')
        if not key:
            return jsonify({'success': False, 'message': 'Key is required'}), 400
            
        keyauthapp.license(key)
        return jsonify({'success': True, 'message': 'Key validated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 401

@app.route('/api/marketplace/process', methods=['POST'])
def process_marketplace():
    try:
        data = request.json
        # Implémentez votre logique de marketplace ici
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)