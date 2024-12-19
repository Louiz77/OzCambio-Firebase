from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()

        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        user_agent = request.headers.get("User-Agent", "Não identificado")

        data["ip"] = client_ip
        data["userAgent"] = user_agent
        data["timestamp"] = firestore.SERVER_TIMESTAMP

        collection_name = "dados_coletados_OZ"
        db.collection(collection_name).add(data)

        return jsonify({"success": "Dados inseridos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insert-init", methods=["POST"])
def insert_data_init():
    try:
        data = request.get_json()

        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        user_agent = request.headers.get("User-Agent", "Não identificado")

        data["ip"] = client_ip
        data["userAgent"] = user_agent
        data["timestamp"] = firestore.SERVER_TIMESTAMP

        if not data:
            return jsonify({"error": "Nenhum dado fornecido"}), 400

        collection_name = "dados_iniciais_coletados_OZ"

        db.collection(collection_name).add(data)

        return jsonify({"success": "Dados inseridos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store-mdns', methods=['POST'])
def store_mdns():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Firestore collection
        print(data)
        ip_user = (data.get("userId"))
        publicIP = (data.get("ip"))

        collection_ref = db.collection(f'mdns_records-{str(ip_user)}')

        collection_ref.add({
            "ipPublic": publicIP,
            "idUser": ip_user,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"message": "Data stored successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)