# Arsitektur Monolith vs Microservices dengan Flask Python

Praktikum membandingkan arsitektur **Monolith** dan **Microservices** menggunakan Flask (Python), dengan studi kasus sederhana: pengelolaan buku dan pemesanan.

- **Mata kuliah:** Paradigma Sistem untuk IT
- **Prodi:** Teknologi Rekayasa Komputer Jaringan, Politeknik Negeri Lhokseumawe
- **Dosen Pengampu:** Muhammad Reza Zulman, S.ST., M.Sc
- **Tanggal Praktikum:** 15 September 2026

## Tujuan

1. Memahami konsep arsitektur Monolith dan Microservices.
2. Membuat aplikasi sederhana menggunakan Flask.
3. Menguji pengelolaan buku dan pemesanan pada aplikasi Monolith.
4. Memisahkan aplikasi menjadi beberapa layanan (Microservices).
5. Memahami perbedaan Monolith vs Microservices dan konsep *fault isolation*.

## Alat dan Bahan

- Laptop/PC (Windows)
- Visual Studio Code
- Python
- Flask dan Requests
- Postman
- PowerShell / Terminal

Instalasi library:

```bash
pip install flask requests
```

## Struktur File

```
praktikum-flask/
├── monolith_app.py     # Monolith (port 5000)
├── book_service.py     # Book Service (port 5001)
└── order_service.py    # Order Service (port 5002)
```

---

## Langkah Kerja: Monolith

Seluruh fitur (buku dan pesanan) berada dalam satu file: `monolith_app.py`.

### 1. Jalankan aplikasi

Masuk ke folder proyek terlebih dahulu, lalu jalankan:

```bash
cd praktikum-flask
python monolith_app.py
```

Aplikasi berjalan di `http://127.0.0.1:5000`.

### 2. Uji `GET /books`

Menampilkan data buku.

```bash
curl http://127.0.0.1:5000/books
```

### 3. Uji `POST /orders`

Membuat pesanan dengan body JSON `{"book_id": 1}`.

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/orders" -Method POST -ContentType "application/json" -Body '{"book_id":1}'
```

Hasil yang diharapkan:

```
book_id id status
------- -- ------
      1  1 berhasil
```

---

## Langkah Kerja: Microservices

Aplikasi dipisah menjadi dua service yang berjalan sendiri-sendiri dan berkomunikasi lewat HTTP.

| Service | File | Port | Endpoint |
|---|---|---|---|
| Book Service | `book_service.py` | 5001 | `/books` |
| Order Service | `order_service.py` | 5002 | `/orders` |

### 1. Jalankan Book Service

Buka terminal pertama:

```bash
python book_service.py
```

### 2. Jalankan Order Service

Buka terminal kedua:

```bash
python order_service.py
```

### 3. Uji Book Service

```bash
curl http://127.0.0.1:5001/books
```

Hasil:

```json
[
  { "id": 1, "stock": 5, "title": "Belajar Flask" }
]
```

### 4. Uji Order Service

Lewat PowerShell:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5002/orders" -Method POST -ContentType "application/json" -Body '{"book_id":1}'
```

Atau lewat Postman:

- Method: `POST`
- URL: `http://127.0.0.1:5002/orders`
- Body: raw, JSON

```json
{
  "book_id": 1
}
```

Hasil: status `201 Created`

```json
{
  "book_id": 1,
  "id": 1,
  "status": "berhasil"
}
```

### 5. Uji Fault Isolation

1. Hentikan Book Service (`CTRL+C` pada terminalnya).
2. Kirim kembali `POST /orders` ke Order Service (port 5002).
3. Order Service **tetap berjalan** dan mengembalikan pesan error:

```json
{
  "error": "Book Service sedang down!"
}
```

Artinya gangguan pada satu service tidak langsung menghentikan service lainnya.

---

## Perbandingan Monolith dan Microservices

| Aspek | Monolith | Microservices |
|---|---|---|
| Struktur | Satu aplikasi | Beberapa service |
| File | `monolith_app.py` | `book_service.py` dan `order_service.py` |
| Port | 5000 | 5001 dan 5002 |
| Komunikasi | Langsung dalam aplikasi | Melalui HTTP |
| Gangguan | Berada dalam satu aplikasi | Dapat diisolasi antar-service |

## Kesimpulan

Monolith menggabungkan semua fitur dalam satu aplikasi, sedangkan Microservices memisahkannya menjadi beberapa service yang berjalan terpisah. Pengujian dengan Postman dan PowerShell menunjukkan pengambilan data buku dan pemesanan berjalan baik. Pada uji fault isolation, Order Service tetap hidup saat Book Service dihentikan dan memberikan pesan error. Kekurangannya, Microservices menambah kompleksitas (mengelola banyak service, potensi masalah koneksi dan *network latency*).

## Troubleshooting

- **`can't open file ... monolith_app.py: No such file or directory`**: kamu belum berada di folder proyek. Jalankan `cd praktikum-flask` dulu.
- **Postman: `Invalid protocol: post`**: kata `POST` ikut tertulis di kolom URL. Pilih method lewat dropdown, dan isi URL hanya `http://127.0.0.1:5002/orders`.
- **Postman: `ECONNREFUSED 127.0.0.1:5001`**: Book Service belum berjalan atau sedang dihentikan.

## Referensi

- Modul Praktikum Arsitektur Monolith vs Microservices dengan Flask Python
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/)
- [Postman Documentation](https://learning.postman.com/docs/)
