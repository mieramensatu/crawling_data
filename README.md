# Traveloka Bus Crawler

Alat otomatis untuk mengambil data jadwal, harga, dan kapasitas bis rute Jakarta–Yogyakarta dari Traveloka menggunakan Selenium.

## Fitur

- Scroll otomatis untuk memuat semua data bis
- Ekstraksi informasi:
  - Nama operator bis
  - Tipe bis
  - Waktu keberangkatan & kedatangan
  - Durasi perjalanan
  - Harga tiket
  - Kapasitas kursi (via klik detail)
- Penyimpanan ke file Excel dan CSV
- Output log yang natural, tidak kaku, dan mudah dipahami

> Catatan: Kolom `star_rating` sengaja tidak disertakan.

## Struktur Proyek

```
traveloka-bus-crawler/
├── main.py
├── config/
│   └── routes.py
├── core/
│   ├── driver.py
│   ├── scroller.py
│   └── extractor.py
├── crawler/
│   └── with_scroll.py
├── storage/
│   └── saver.py
├── utils/
│   └── helpers.py     
└── output/ 
```

## Persyaratan

- Python 3.8+
- Chrome dan ChromeDriver terinstal
- Package Python:
  - `selenium`
  - `pandas`
  - `openpyxl`

### Instalasi

Jalankan perintah berikut di terminal:

`
pip install selenium pandas openpyxl
`

Pastikan `chromedriver` ada di PATH sistem, atau sesuaikan `webdriver.Chrome()` dengan path eksplisit jika diperlukan.

## Cara Menjalankan

1. Buka terminal di folder proyek
2. Jalankan:

`
python main.py
`

Proses akan:
- Membuka Traveloka untuk rute Jakarta–Yogyakarta (jadwal besok)
- Scroll otomatis hingga semua data termuat
- Klik setiap kontainer bis untuk ambil kapasitas kursi
- Simpan hasil ke folder `output/` dalam format `.xlsx` dan `.csv`

## Contoh Output

File hasil bernama seperti:
- `nama bis_25-11-2025_143022.xlsx`
- `nama bis_25-11-2025_143022.csv`

Isi kolom:
- platform
- route_name
- route_date
- route_link
- bus_name
- bus_type
- departing_time
- reaching_time
- duration
- price
- seat_capacity
- crawl_timestamp

## Catatan Pengembangan

- Proyek dirancang modular untuk memudahkan penambahan rute atau moda transportasi lain.
- Fungsi debug tersedia di folder `debug/` (tidak aktif secara default).
- Tidak menggunakan Streamlit atau antarmuka web — fokus pada CLI dan file output.

## Lisensi

Proyek ini untuk keperluan pembelajaran dan pengembangan pribadi.
