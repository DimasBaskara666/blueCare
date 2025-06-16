# Panduan Kontribusi

Terima kasih atas minat Anda untuk berkontribusi pada proyek Sistem Deteksi Penyakit Berbasis NLP! Berikut adalah panduan untuk membantu Anda berkontribusi dengan efektif.

## 🎯 Cara Berkontribusi

1. **Fork & Clone**

   - Fork repositori ini
   - Clone fork Anda ke lokal

   ```bash
   git clone https://github.com/YOUR_USERNAME/bismillahPakar.git
   ```

2. **Setup Development**

   - Backend:
     ```bash
     cd backend
     python -m venv venv
     source venv/bin/activate  # Linux/Mac
     .\venv\Scripts\activate   # Windows
     pip install -r requirements.txt
     ```
   - Frontend:
     ```bash
     cd frontend
     npm install
     ```

3. **Branch**

   - Buat branch baru untuk fitur/perbaikan

   ```bash
   git checkout -b feature/nama-fitur
   ```

4. **Development**

   - Ikuti standar kode yang ada
   - Tambahkan test untuk fitur baru
   - Update dokumentasi jika diperlukan

5. **Commit**

   - Gunakan commit message yang jelas
   - Format: `tipe(scope): deskripsi`
   - Contoh: `feat(auth): add login functionality`

6. **Push & Pull Request**
   - Push ke fork Anda
   - Buat Pull Request ke branch `main`

## 📝 Standar Kode

### Python (Backend)

- Gunakan PEP 8
- Maksimal 88 karakter per baris
- Gunakan type hints
- Dokumentasikan fungsi dengan docstring

### TypeScript (Frontend)

- Gunakan ESLint & Prettier
- Ikuti konvensi React/Next.js
- Gunakan TypeScript strict mode
- Dokumentasikan komponen dengan JSDoc

## 🧪 Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## 📚 Dokumentasi

- Update README.md jika ada perubahan signifikan
- Dokumentasikan API di `backend/docs/api.md`
- Tambahkan komentar untuk kode kompleks

## 🔍 Review Process

1. Semua PR akan direview
2. Pastikan semua test passed
3. Pastikan tidak ada konflik
4. Tunggu approval dari maintainer

## 📋 Checklist PR

- [ ] Kode mengikuti standar
- [ ] Test ditambahkan/diupdate
- [ ] Dokumentasi diupdate
- [ ] Tidak ada error linting
- [ ] Semua test passed

## 🤝 Komunikasi

- Gunakan issue tracker untuk diskusi
- Jaga komunikasi profesional
- Hormati semua kontributor

## 📄 Lisensi

Dengan berkontribusi, Anda setuju untuk melepaskan kontribusi Anda di bawah lisensi MIT.
