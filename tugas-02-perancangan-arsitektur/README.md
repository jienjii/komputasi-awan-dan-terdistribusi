# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok

1. Pilih **satu** gaya arsitektur utama: **Service-Oriented Architecture (SOA)** atau **Publish-Subscribe**. Boleh dikombinasikan (mis. SOA untuk service inti + Pub-Sub untuk notifikasi), tapi harus dijustifikasi kenapa kombinasi ini yang dipilih.
2. Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
3. Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan **jenis komunikasinya** (sinkron/asinkron, request-response/event).
4. Analisis tertulis: kenapa gaya ini mengatasi masalah *coupling* dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).

## Cara Membuat Diagram (Gratis, Cukup Laptop)

Tidak perlu software berbayar. Dua opsi:

**Opsi A — Mermaid di dalam Markdown (disarankan).** Ditulis sebagai teks biasa di `README.md`, otomatis dirender jadi diagram oleh GitHub — tidak perlu install apa pun.

## Diagram Arsitektur FoodGo

```mermaid
graph TD
    %% Client & Gateway
    Client["📱 Pelanggan"] -->|Sinkron: HTTP API| Gateway["🌐 API Gateway"]

    %% Core SOA Services
    subgraph Core_SOA ["Layanan Inti (SOA)"]
        Gateway -->|Sinkron: route request| OrderSvc["📦 Service Pesanan"]
        OrderSvc -->|"Sinkron: validasi menu (timeout 3s, CB)"| RestoSvc["🍔 Service Katalog Resto"]
        OrderSvc -->|"Sinkron: proses bayar (timeout 3s, CB)"| PaymentSvc["💳 Service Pembayaran"]
    end

    %% Database Isolation
    OrderSvc --- DB_Order[("Database Pesanan")]
    PaymentSvc --- DB_Pay[("Database Pembayaran")]
    RestoSvc --- DB_Resto[("Database Katalog")]

    %% Event Broker
    Broker[("📥 Message Broker\n(RabbitMQ / Kafka)")]

    %% Service Async
    CourierSvc["🛵 Service Kurir & Notifikasi"]
    CourierSvc --- DB_Courier[("Database Kurir")]

    %% Asynchronous Event Streams
    OrderSvc -.->|publish PesananDibayar| Broker
    Broker -.->|subscribe PesananDibayar| RestoSvc

    RestoSvc -.->|"publish PesananDiterima / Ditolak"| Broker
    Broker -.->|subscribe PesananDiterimaResto| CourierSvc
    
    CourierSvc -.->|publish KurirDitugaskan| Broker
    Broker -.->|subscribe KurirDitugaskan / PesananDitolak| OrderSvc
    Broker -.->|"subscribe PesananDitolak (Refund)"| PaymentSvc

    %% Real-time Tracking
    OrderSvc -.->|push SSE status| Client
```

**Legenda Diagram:**
* **Garis Solid (`-->`):** Komunikasi Sinkron (Request-Response / Direct Call).
* **Garis Putus-Putus (`-.->`):** Komunikasi Asinkron (Event-Driven via Message Broker / SSE).
* *Batas Arsitektur:* Layanan Inti menggunakan komunikasi SOA/REST untuk transaksi real-time, sedangkan koordinasi antar-modul resto, kurir, dan pesanan berbasis Publish-Subscribe secara asinkron.
  
tugas-02-perancangan-arsitektur/
├── README.md          # Analisis + diagram Mermaid (jika Opsi A) atau referensi ke diagram/
├── JURNAL.md
└── diagram/            # File .png/.drawio jika pakai Opsi B
```

## Rubrik Penilaian (Tugas 2)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan gaya arsitektur | 20% | Justifikasi SOA/Pub-Sub sesuai kebutuhan *decoupling* di skenario |
| Kelengkapan & kejelasan diagram | 30% | Semua komponen kunci ada, jenis komunikasi (sinkron/asinkron) jelas ditandai |
| Analisis trade-off | 30% | Bukan hanya kelebihan — kekurangan/kompleksitas baru juga dibahas |
| Proses & kontribusi kelompok | 20% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh memakai AI untuk brainstorming komponen apa saja yang umum ada di gaya arsitektur SOA/Pub-Sub; **tidak boleh** meminta AI menggambar diagram final atau menuliskan analisis trade-off yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Diagram Mermaid/draw.io yang "terlalu generik" (identik dengan contoh tutorial di internet tanpa penyesuaian ke kasus FoodGo) akan dinilai rendah pada komponen kelengkapan & kejelasan diagram.
