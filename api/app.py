from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import validate_token

app = Flask(__name__)
CORS(app)

@app.route('/reports', methods=['GET'])
def get_report():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if not token:
        return jsonify({"error": "auth error"}), 401

    user_info = validate_token(token)
    if not user_info:
        return jsonify({"error": "auth error"}), 401

    roles = user_info.get("realm_access", {}).get("roles", [])
    if "prothetic_user" not in roles:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({
        "report": {
            "text":"some values"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)