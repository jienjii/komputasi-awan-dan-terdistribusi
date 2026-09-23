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

## Pitfall 2: [Bandwidth Tidak Terbatas] — ditulis oleh [sefia nuraini]

**Bukti di skenario:** Waktu bikin fitur tracking order real-time, tim front-end nulis kode yang manggil API status pesanan tiap request langsung dianggap "instant", jadi mereka pasang polling tiap 1 detik ke service tracking tanpa mikirin delay jaringan. Di local testing semua kelihatan lancar-lancar aja karena latency-nya emang deket ke nol.

**Kenapa ini keliru:** Latency itu nggak pernah benar-benar nol, apalagi kalau requestnya lintas server, lintas region, atau lewat internet publik (misal user pakai jaringan seluler). Yang keliatan cepat pas testing di localhost bisa jadi jauh lebih lambat begitu dipakai di kondisi nyata, apalagi kalau ada banyak hop antar service (order -> tracking -> notifikasi -> dsb).

Dampak ke FoodGo: Polling tiap 1 detik dari ribuan user yang lagi nunggu makanannya bikin beban ke service tracking numpuk parah, padahal responnya sendiri belum tentu balik secepat itu. Ujung-ujungnya request numpuk di antrian, delay makin kerasa, dan user malah lihat status pesanan "nyangkut" atau telat update padahal driver udah jalan.

**Solusi desain awal:**
Ganti pendekatan polling jadi push-based (pakai WebSocket atau server-sent events) supaya update status dikirim cuma pas ada perubahan, bukan ditanya terus-terusan
Kalau tetap butuh polling, naikkan interval nya dan bikin adaptif (misal makin lama makin jarang kalau nggak ada perubahan status)
Tambahin caching di sisi client/edge buat status yang nggak berubah-ubah cepat

Trade-off: Push-based butuh effort lebih buat maintain koneksi persisten (WebSocket) dan lebih ribet pas scaling horizontal dibanding REST biasa. Kalau adaptif polling yang dipilih, ada resiko user ngerasa update-nya "telat" karena interval yang makin melebar.
## Pitfall 3: [Jaringan Aman / The Network is Secure] — ditulis oleh [sefia nuraini/]

**Bukti di skenario:** Komunikasi antar-modul di FoodGo (pesanan, pembayaran, notifikasi) dilakukan lewat HTTP biasa tanpa enkripsi, dan tidak ada mekanisme autentikasi/otorisasi antar-service—modul pembayaran menerima begitu saja request yang "mengaku" datang dari modul pesanan tanpa validasi lebih lanjut.

**Kenapa ini keliru:** Asumsi bahwa jaringan internal itu otomatis aman adalah kekeliruan klasik, apalagi di era arsitektur terdistribusi/cloud di mana traffic bisa melewati banyak segmen jaringan, container, bahkan region berbeda. Tanpa enkripsi (TLS) dan autentikasi antar-service (misalnya mTLS atau API key/token), siapa pun yang berhasil menyusup ke jaringan internal bisa menyadap data sensitif atau bahkan menyamar sebagai service lain untuk mengirim request palsu.

**Dampak ke FoodGo:** Data sensitif seperti informasi pembayaran, nomor kartu, atau data pribadi user bisa disadap (man-in-the-middle) kalau ada pihak tidak sah yang berhasil masuk ke jaringan internal. Selain itu, tanpa autentikasi antar-service, ada risiko pihak eksternal mengirim request palsu langsung ke modul pembayaran untuk membuat transaksi ilegal atau memanipulasi status pesanan tanpa melalui modul pesanan yang sah.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
