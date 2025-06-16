# Sistem Deteksi Penyakit Berbasis NLP (Bahasa Indonesia)

Sistem deteksi penyakit berbasis web yang menggunakan Natural Language Processing (NLP) untuk menganalisis gejala dalam Bahasa Indonesia dan memberikan prediksi penyakit potensial.

## 🚀 Fitur Utama

- **Deteksi Penyakit Berbasis Gejala**

  - Input gejala dalam Bahasa Indonesia
  - Analisis menggunakan model machine learning
  - Prediksi penyakit dengan tingkat kepercayaan

- **Input Suara**

  - Dukungan input suara menggunakan Web Speech API
  - Konversi suara ke teks dalam Bahasa Indonesia
  - Aksesibilitas untuk pengguna lanjut usia

- **Asisten Kesehatan (Chatbot)**

  - Tanya jawab interaktif
  - Klarifikasi gejala
  - Panduan kesehatan umum

- **Visualisasi Hasil**
  - Skor kepercayaan untuk setiap prediksi
  - Highlight kata kunci/gejala
  - Timeline perkembangan gejala
  - Saran tindakan lanjutan

## 🛠️ Teknologi

### Backend

- Python 3.x
- Flask (RESTful API)
- NLTK + Sastrawi (NLP Bahasa Indonesia)
- Scikit-learn (Klasifikasi)
- FastText/IndoBERT (Opsional)

### Frontend

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Web Speech API
- Framer Motion

## 🏗️ Struktur Proyek

```
disease-detector-app/
├── backend/          # Flask API & Model
├── frontend/         # Next.js Application
└── docs/            # Dokumentasi
```

## 🚀 Memulai

### Prasyarat

- Python 3.x
- Node.js 18+
- npm/yarn

### Instalasi Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
python run.py
```

### Instalasi Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 Penggunaan

1. Buka aplikasi di browser (http://localhost:3000)
2. Masukkan gejala melalui teks atau suara
3. Ikuti panduan chatbot untuk klarifikasi
4. Lihat hasil prediksi dan rekomendasi

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan buat pull request atau buka issue untuk diskusi.

## 📄 Lisensi

MIT License - lihat [LICENSE](LICENSE) untuk detail.

## ⚠️ Disclaimer

Sistem ini hanya untuk tujuan pendidikan dan screening awal. Selalu konsultasikan dengan profesional kesehatan untuk diagnosis yang akurat.
