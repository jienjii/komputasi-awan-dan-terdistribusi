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

graph TD
    Pelanggan[📱 Pelanggan / Mobile App] -->|1. HTTP REST Request - Sinkron| APIGateway[🌐 API Gateway]
    APIGateway -->|2. Route Request - Sinkron| OrderSvc[📦 Modul Pesanan / Order Service]

    %% Jalur Validasi & Bayar (Sinkron - SOA)
    OrderSvc -->|3. Validasi Menu & Harga - REST/gRPC Sinkron| RestoSvc[📖 Modul Katalog Resto]
    OrderSvc -->|4. Proses Otorisasi Bayar - REST/gRPC Sinkron| PaymentSvc[💳 Modul Pembayaran]

    %% Jalur Notifikasi & Kurir (Asinkron - Pub/Sub) -> Solusi agar tidak saling mengganggu
    OrderSvc -->|5. Publish Event: OrderPaid - Asinkron| Broker[(📥 Message Broker)]
    
    %% Distribusi Event dari Broker ke Subscriber
    Broker -->|6. Kirim Pesanan Masuk| AppResto[🏪 App Resto]
    Broker -->|7. Trigger Dispatch & Push Notif| CourierSvc[🔔 Modul Kurir & Notifikasi]
    CourierSvc -->|8. Penugasan & Push Notification| AppKurir[🛵 App Kurir]

    %% Pewarnaan agar mirip dengan diagram asli Anda
    style Pelanggan fill:#e6dbfa,stroke:#b39ddb,stroke-width:1px
    style APIGateway fill:#e8f5e9,stroke:#81c784,stroke-width:2px
    style OrderSvc fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style RestoSvc fill:#e3f2fd,stroke:#42a5f5,stroke-width:1px
    style PaymentSvc fill:#e3f2fd,stroke:#42a5f5,stroke-width:1px
    style CourierSvc fill:#fff3e0,stroke:#ffb74d,stroke-width:1px
    style AppResto fill:#e6dbfa,stroke:#b39ddb,stroke-width:1px
    style AppKurir fill:#e6dbfa,stroke:#b39ddb,stroke-width:1px
    style Broker fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px


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

