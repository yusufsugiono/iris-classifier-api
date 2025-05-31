# 🌸 Iris Classifier API with TensorFlow & Firebase

API ini memanfaatkan model machine learning (TensorFlow) untuk melakukan klasifikasi terhadap data bunga Iris berdasarkan fitur-fitur numeriknya. Setiap hasil prediksi disimpan secara otomatis ke Firebase Firestore, dengan menyertakan informasi pengguna (username) yang melakukan prediksi.

Project ini dirancang sebagai demonstrasi integrasi antara model machine learning dan RESTful API, sekaligus menunjukkan bagaimana riwayat prediksi dapat dicatat dan diakses secara real-time melalui Firestore.

## 🚀 Fitur

- Prediksi klasifikasi bunga Iris berdasarkan 4 fitur numerik
- Simpan hasil klasifikasi ke Firestore
- Ambil riwayat klasifikasi berdasarkan `username`

## 🧠 Teknologi yang Digunakan

- Python 3.10
- Flask
- TensorFlow
- Firebase Admin SDK (Firestore)
- Scikit-learn (untuk preprocessing)
- Pickle (untuk menyimpan scaler)
- Swagger (untuk menyediakan dokumentasi API)

---

## ⚙️ Instalasi

### 1. Clone repository

```bash
git clone https://github.com/yusufsugiono/iris-classifier-api.git
cd iris-classifier-api
```

### 2. Buat virtual environment (opsional)

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Instal dependensi

> ⚠️ Gunakan Python 3.10 atau 3.11. TensorFlow belum mendukung Python terbaru saat repositori ini dibuat.

```bash
pip install -r requirements.txt
```

### 4. Setup Firebase

- Buat project Firebase
- Aktifkan Firestore (mode production atau test)
- Generate private key baru melalui menu **Project settings** → **Service accounts** → **Generate new private key**
- Setelah terdownload, rename menjadi `service-account-key.json` dan pindahkan ke folder project ini

---

## 🧪 Menjalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan pada `http://localhost:5000`

---

## 📮 Endpoint API

> 💡 Anda juga dapat membaca dokumentasi dan mencoba memanggil endpoint dengan mengakses http://localhost:5000 pada web browser

### 1. `POST /predict`

Melakukan klasifikasi bunga iris

#### 🔸 Request JSON

```json
{
  "username": "john_doe",
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

#### 🔹 Response JSON

```json
{
  "prediction": "setosa"
}
```

### 2. `GET /history?username=john_doe`

Mendapatkan riwayat klasifikasi berdasarkan username

#### 🔹 Response JSON

```json
{
  "history": [
    {
      "id": "docid123",
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2,
      "predicted_label": "setosa",
      "timestamp": "...",
      "username": "john_doe"
    }
  ]
}
```

---

## 📌 Catatan

- Jika Anda ingin memodifikasi modelnya, maka Anda dapat mengubah kode pada berkas notebook `Iris_Classification_using_Tensorflow.ipynb` kemudian jalankan dan timpa berkas `iris_model.h5` serta `scaler_iris.pkl`yang sudah ada.
- Firestore membutuhkan Composite Index untuk kombinasi username + timestamp. Buat index ini di Firebase Console (Firestore → Indexes → Create).
- Anda dapat mencoba membuka berkas `webapp/index.html` pada browser sebagai contoh sederhana implementasi pada frontend web

---

## 📝 Lisensi

Project ini bebas digunakan untuk tujuan pembelajaran dan pengembangan pribadi.

---

## ✨ Kontribusi

Project ini dikembangkan seadanya saja. Jika kamu merasa ada yang dapat diimprove lebih lanjut maka silahkan untuk mengirimkan pull request maupun saran yang membangun ya. Terimakasih 🤝
