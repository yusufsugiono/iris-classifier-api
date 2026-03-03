from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import joblib
from flasgger import Swagger

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)


# Swagger API Docs
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Klasifikasi Bunga Iris",
        "description": "API sederhana untuk klasifikasi bunga Iris menggunakan TensorFlow",
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
# JSON Request: {sepal_length: float,  sepal_width: float, petal_length: float, petal_width: float}
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
            - sepal_length
            - sepal_width
            - petal_length
            - petal_width
          properties:
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
        description: Success Response
        schema:
          type: object
          properties:
            prediction:
              type: string
              example: setosa
      400:
        description: Bad Request Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing feature sepal_width
    """

    # Ambil body payload
    data = request.get_json()

    # Validasi input
    required_fields = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
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

        # Kirim hasil prediksi sebagai response api
        return jsonify({
            "prediction": predicted_label
        })


    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run server
if __name__ == "__main__":
    app.run(debug=True)
