from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import joblib
import firebase_admin
from firebase_admin import credentials, firestore
from flasgger import Swagger


# Inisialisasi Firebase
cred = credentials.Certificate("service-account-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)


# Swagger API Docs
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Klasifikasi Bunga Iris",
        "description": "API sederhana untuk klasifikasi bunga Iris menggunakan TensorFlow & Firebase",
        "version": "1.0.0",
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"]
}

swagger = Swagger(app, template=swagger_template)


# Load model dan scaler
model = tf.keras.models.load_model("iris_model.h5")
scaler = joblib.load("scaler_iris.pkl")

# Label
class_names = ['setosa', 'versicolor', 'virginica']


# Endpoint root menampilkan pesan selamat datang
# GET http://localhost:5000/
@app.route("/")
def home():
    return redirect('/apidocs')


# Endpoint untuk prediksi hasil klasifikasi
# POST http://localhost:5000/predict
# JSON Request: {username: string, sepal_length: float,  sepal_width: float, petal_length: float, petal_width: float}
# JSON response: {prediction: string}
@app.route("/predict", methods=["POST"])
def predict():
    """
    Prediksi jenis bunga Iris
    ---
    tags:
      - Prediksi
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - sepal_length
            - sepal_width
            - petal_length
            - petal_width
          properties:
            username:
              type: string
              example: john_doe
            sepal_length:
              type: number
              example: 5.1
            sepal_width:
              type: number
              example: 3.5
            petal_length:
              type: number
              example: 1.4
            petal_width:
              type: number
              example: 0.2
    responses:
      200:
        description: Prediksi berhasil
        schema:
          type: object
          properties:
            prediction:
              type: string
              example: setosa
    """

    # Ambil body payload
    data = request.get_json()

    # Validasi input
    required_fields = ["username", "sepal_length", "sepal_width", "petal_length", "petal_width"]
    # Ketika tidak ada data json yg dikirim:
    if not data:
        return jsonify({"error": "Body payload required"}), 400

    # Ketika isi json ada yg kurang:
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing feature: {', '.join(missing)}"}), 400

    try:
        # Ambil dan susun fitur sesuai urutan
        features = [
            data["sepal_length"],
            data["sepal_width"],
            data["petal_length"],
            data["petal_width"]
        ]

        # Bungkus data agar sesuai bentuk input ke model
        input_data = np.array([features])
        input_scaled = scaler.transform(input_data)

        # Predict dengan modal yg sudah di load
        prediction = model.predict(input_scaled)
        predicted_index = int(np.argmax(prediction))
        predicted_label = class_names[predicted_index]

        # Prepare data history untuk disimpan ke firebase
        history = {
            "username": data["username"],
            "sepal_length": float(data["sepal_length"]),
            "sepal_width": float(data["sepal_width"]),
            "petal_length": float(data["petal_length"]),
            "petal_width": float(data["petal_width"]),
            "predicted_label": predicted_label,
            "timestamp": firestore.SERVER_TIMESTAMP
        }

        # Simpan ke Firestore
        db.collection("classification_history").add(history)

        # Kirim hasil prediksi sebagai response api
        return jsonify({
            "prediction": predicted_label
        })


    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint untuk tampilkan riwayat prediksi
# GET http://localhost:5000/history?username=john_doe
@app.route("/history", methods=["GET"])
def get_history():
    """
    Ambil seluruh riwayat klasifikasi berdasarkan username
    ---
    tags:
      - Riwayat
    parameters:
      - name: username
        in: query
        type: string
        required: true
        description: Username yang ingin diambil riwayatnya
        example: john_doe
    responses:
      200:
        description: Daftar riwayat klasifikasi
        schema:
          type: object
          properties:
            history:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: abc123docid
                  username:
                    type: string
                    example: john_doe
                  sepal_length:
                    type: number
                    example: 5.1
                  sepal_width:
                    type: number
                    example: 3.5
                  petal_length:
                    type: number
                    example: 1.4
                  petal_width:
                    type: number
                    example: 0.2
                  predicted_label:
                    type: string
                    example: setosa
                  timestamp:
                    type: string
                    example: 2025-05-29T12:00:00Z
      400:
        description: Parameter username tidak disertakan
      404:
        description: Data riwayat atau username tidak ditemukan
      500:
        description: Terjadi kesalahan saat mengambil data
    """
    # Ambil parameter username
    username = request.args.get("username")

    # Validasi jika tidak ada username
    if not username:
        return jsonify({"error": "Username required"}), 400

    try:
        # Query ke firebase, filter berdasarkan username
        docs = db.collection("classification_history") \
                 .where("username", "==", username) \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .stream()

        # Bungkus ke dalam python list
        history = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            history.append(data)

        # Kirimkan hasilnya
        if len(history) > 0:
            return jsonify({"history": history})
        else:
            return jsonify({"message": "Data Not Found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run server
if __name__ == "__main__":
    app.run(debug=True)
