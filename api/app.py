from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import check_role

app = Flask(__name__)
CORS(app)

@app.route('/reports', methods=['GET'])
def get_report():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if not token:
        return jsonify({"error": "token error"}), 401

    if not check_role(token, "prothetic_user"):
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({
        "report": {
            "text":"some values"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)