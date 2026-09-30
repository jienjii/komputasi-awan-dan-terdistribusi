# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [Kelompok 14]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Angeli Thie] | [103072400032] | [] |
| [Sefia Nuraini] | [103072400043] | [] |
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

## Pitfall 2: [Bandwidth Tidak Terbatas] — ditulis oleh [Sefia Nuraini]

**Bukti di skenario:** Waktu bikin fitur tracking order real-time, tim front-end nulis kode yang manggil API status pesanan tiap request langsung dianggap "instant", jadi mereka pasang polling tiap 1 detik ke service tracking tanpa mikirin delay jaringan. Di local testing semua kelihatan lancar-lancar aja karena latency-nya emang deket ke nol.

**Kenapa ini keliru:** Latency itu nggak pernah benar-benar nol, apalagi kalau requestnya lintas server, lintas region, atau lewat internet publik (misal user pakai jaringan seluler). Yang keliatan cepat pas testing di localhost bisa jadi jauh lebih lambat begitu dipakai di kondisi nyata, apalagi kalau ada banyak hop antar service (order -> tracking -> notifikasi -> dsb).

**Dampak ke FoodGo:** Polling tiap 1 detik dari ribuan user yang lagi nunggu makanannya bikin beban ke service tracking numpuk parah, padahal responnya sendiri belum tentu balik secepat itu. Ujung-ujungnya request numpuk di antrian, delay makin kerasa, dan user malah lihat status pesanan "nyangkut" atau telat update padahal driver udah jalan.

**Solusi desain awal:**
Ganti pendekatan polling jadi push-based (pakai WebSocket atau server-sent events) supaya update status dikirim cuma pas ada perubahan, bukan ditanya terus-terusan
Kalau tetap butuh polling, naikkan interval nya dan bikin adaptif (misal makin lama makin jarang kalau nggak ada perubahan status)
Tambahin caching di sisi client/edge buat status yang nggak berubah-ubah cepat

**Trade-off**: Push-based butuh effort lebih buat maintain koneksi persisten (WebSocket) dan lebih ribet pas scaling horizontal dibanding REST biasa. Kalau adaptif polling yang dipilih, ada resiko user ngerasa update-nya "telat" karena interval yang makin melebar.

---

## Bagian 3: [High Availability & Fault Tolerance] — ditulis oleh [Angeli Thie]

### 1. Perancangan Load Balancer & Horizontal Scaling 
* **Pendekatan:** Menerapkan *Layer 7 Load Balancer* (misalnya NGINX / HAProxy) di depan *Order Service* dan *Payment Service*
* **Mekanisme Scaling:** Setiap *microservice* disiapkan untuk berjalan minimal dalam 2 instance (*redundancy*) untuk menghilangkan *Single Point of Failure* (SPOF). *Load Balancer* mendistribusikan lalu lintas menggunakan algoritma *Round Robin* atau *Leasy Connections*
* **Health Checking:** *Load Balancer* melakukan *active health check* berkala ke *endpoint* `/health` tiap *service*. Jika satu instance gagal/down, lalu lintas secara otomatis dialihkan ke instance yang sehat (*auto-failover*)

### 2. Pattern Fault Tolerance (Timeout, Retry, & Circuit Breaker)
* **Timeout:** 
    * Semua panggilan *synchronous* antar-layanan (misal: *Order Service* ke *Payment Service*) dibatasi *timeout* maksimal **3 detik**
    * Jika tidak ada respons dalam 3 detik, *Order Service* membatalkan panggilan tersebut dan mengembalikan *fallback response* ke pengguna daripada menunggu tanpa batas (*hang*)
* **Exponential Backoff Retry with Jitter:**
    * Untuk mengatasi kegagalan sementara (*transient failure*), diterapkan *retry* maksimal **3 kali**
    * Waktu jeda antar *retry* meningkat secara eksponensial (misal: 1 detik, 2 detik, 4 detik) ditambah variasi acak (*jitter*) untuk mencegah kondisi *retry storm* (penumpukan *request* simultan yang memperparah beban server tujuan)
* **Circuit Breaker Point:**
    * Menerapkan *Circuit Breaker* (misal menggunakan Resillence4j/Envoy) pada komunikasi ke *Payment Service*
    * Jika rasio kegagalan mencapai >50% dalam rentang 10 detik, status *circuit breaker* berubah menjadi **Open**. Panggilan berikutnya akan langsung ditolak secara lokal (*fast-fail*) tanpa membebankan *Payment Service*, serta mengembalikan pesan bahwa metode pembayaran sedang tidak stabil. Setelah rentang *cooldown* tertentu, status masuk ke **Half-open** untuk menguji pemulihan layanan secara parsial
## Bagian 4: [Keamanan Inter-Service & Zero Trust] - ditulis oleh [Angeli Thie]

### 1. Enkripsi Transport
* Menggunakan HTTPS untuk komunikasi antar service

---

## Kesimpulan Kelompok
