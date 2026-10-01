# WAD05-Cakrawala

Tugas Web Application Development, Universitas Cakrawala.

- Nama: Dharma Satriadi
- NIM: 25120300030

## Isi repo

- `tugas_1`: dokumen jawaban dan live search tugas pertama. Buka berkas HTML langsung di browser.
- `tugas_2`: dashboard Vue 3 dengan detail pengguna dan pengurutan nama.
- `tugas_uts`: dashboard inventaris Vue 3 dan FastAPI. Cara menjalankan ada di `tugas_uts/README.md`.

## Menjalankan tugas kedua

```bash
cd tugas_2
npm install
npm run dev
```

Klik **Muat Pengguna** untuk mengambil data dari JSONPlaceholder. Cari berdasarkan username, misalnya `agussetiawan`. Email mengikuti username dengan domain `@jiep.co.id`, misalnya `agussetiawan@jiep.co.id`.

Tombol **Lihat Detail** menampilkan telepon, perusahaan, dan kota. Tombol **Urutkan A-Z** dan **Urutkan Z-A** mengurutkan hasil pencarian berdasarkan nama.

Untuk memeriksa build, jalankan `npm run build` di folder `tugas_2`.
