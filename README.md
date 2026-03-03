# 🌸 Iris Classifier API with TensorFlow

API ini memanfaatkan model machine learning (TensorFlow) untuk melakukan klasifikasi terhadap data bunga Iris berdasarkan fitur-fitur numeriknya.

Project ini dirancang sebagai demonstrasi integrasi antara model machine learning dan REST API.

> ℹ️ Branch ini memuat source code Iris Classifier API tanpa integrasi Firebase untuk menyimpan hasil klasifikasi

> ℹ️ Jika Anda ingin mempelajari fitur tambahan untuk integrasi ke Firebase, silakan menuju branch [main](https://github.com/yusufsugiono/iris-classifier-api/tree/main)

## 🚀 Fitur

- Prediksi klasifikasi bunga Iris berdasarkan 4 fitur numerik

## 🧠 Teknologi yang Digunakan

- Python 3.10
- Flask
- TensorFlow
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

> 💡Jika Anda menginstal Python dengan versi selain 3.10 maka direkomendasikan untuk memakai [Conda](https://www.anaconda.com/docs/main) untuk membuat virtual environment dengan versi spesifik Python 3.10 karena TensorFlow belum mendukung Python terbaru saat repositori ini dibuat.
> ```bash
> conda create -n iris-api-env python=3.10
> conda activate iris-api-env
>```
>


### 3. Instal dependensi

```bash
pip install -r requirements.txt
```

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
---

## 📌 Catatan

- Jika Anda ingin memodifikasi modelnya, maka Anda dapat mengubah kode pada berkas notebook `Iris_Classification_using_Tensorflow.ipynb` kemudian jalankan dan timpa berkas `iris_model.h5` serta `scaler_iris.pkl`yang sudah ada.
- Anda dapat mencoba membuka berkas `webapp/index.html` pada browser sebagai contoh sederhana implementasi pada frontend web

---

## 📝 Lisensi

Project ini bebas digunakan untuk tujuan pembelajaran dan pengembangan pribadi.

---

## ✨ Kontribusi

Project ini dikembangkan seadanya saja. Jika kamu merasa ada yang dapat diimprove lebih lanjut maka silahkan untuk mengirimkan pull request maupun saran yang membangun ya. Terimakasih 🤝
