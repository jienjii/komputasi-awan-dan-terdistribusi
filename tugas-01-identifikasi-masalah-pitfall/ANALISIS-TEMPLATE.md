# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [Kelompok 14]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Angeli Thie] | [103072400032] | [Analisis Pitfall 1 (The Network is Reliable)] |
| [Sefia Nuraini] | [103072400043] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [The Network is Reliable] — ditulis oleh [Angeli Thie]

**Bukti di skenario:** [Tim menemukan bahwa kode mereka menulis asumsi seperti "# network is always reliable, no need for retry" dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)]

**Kenapa ini keliru:** [Jaringan dalam sistem terdistribusi pada kenyataannya bersifat unreliable (tidak dapat diandalkan 100%). Koneksi dapat terputus, mengalami packet loss, high latency, atau layanan tujuan mengalami masalah sementara. Berasumsi bahwa panggilan jaringan selalu berhasil dan pasti merespons secara instan membuat aplikasi rentan mengalami hang atau deadlock]

**Dampak ke FoodGo:** [Saat modul pembayaran mengalami gangguan atau keterlambatan merespons, modul pesanan akan blocking (menunggu tanpa batas waktu/tanpa timeout). Hal ini menyebabkan pemakaian thread/connection pool terus menumpuk di modul pesanan hingga akhirnya server kehabisan resource dan crash]

**Solusi desain awal:** [
    1. Menerapkan Timeout pada setiap panggilan jaringan antar-layanan (misalnya batas maksimal 3-5 detik)
    2. Menerapkan strategi Retry with Exponential Backoff and Jitter untuk menangani kegagalan sementara (transient failure)
    3. Mengintegrasikan pola Circuit Breaker untuk memutus panggilan ke layanan pembayaran secara otomatis jika tingkat kegagalannya melampaui ambang batas tertentu
]

**Trade-off:** [Penerapan retry dapat memperparah beban pada layanan target yg sedang overloaded (cascading failure atau retry storm). Penggunaan Circuit Breaker juga berisiko menolak transaksi pengguna secara instan jika parameter threshold kurang tepat]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
