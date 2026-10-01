# Dashboard Inventaris Klinik Bedah Plastik Estetika

Tugas UTS Dharma Satriadi (25120300030). Data barang merupakan contoh simulasi, bukan stok resmi perusahaan.

## Menjalankan

Jalankan perintah berikut dari root repo `Tugas_DS/` dengan Python 3.10+ dan Node.js terpasang.

Backend:

```bash
cd tugas_uts/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Frontend, di terminal lain:

```bash
cd tugas_uts/frontend
npm install
npm run dev
```

Buka `http://127.0.0.1:5174`. Dokumentasi API tersedia di `http://127.0.0.1:8001/docs`.

Status stok: **Habis** untuk 0 unit, **Menipis** untuk 1–5 unit, dan **Aman** untuk lebih dari 5 unit. Data awal berisi 20 barang dari `backend/seed_barang.json`. Perubahan selama aplikasi berjalan disimpan dalam memori dan kembali ke data awal saat backend dimulai ulang.
