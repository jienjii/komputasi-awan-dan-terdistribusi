# Jurnal Proses — Tugas 2

## [30 September 2026]
- Opsi arsitektur yang dipertimbangkan: ...
- Kenapa akhirnya pilih [SOA/Pub-Sub]: ...
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 30/9/2026 | Gemini | "Berikan Outline dasar untuk High Availability dan Resilience pada sistem terdistribusi" | AI memberikan poin umum tentang Load Balancer, Auto Scaling, Timeout, dan Retry | Menulis poin-poin tersebut sebagai draf kasar awal, namun menyadari bahwa solusi ini masih terlalu umum dan berisiko over-engineering |
| 30/9/2026 | Gemini | "Bagaimana mencegah retry storm pada kegagalan komunikasi inter-service dan bagaimana konfigurasi threshold Circuit Breaker yg pas?" | AI menyarankan penggunaan Exponential Backoff dengan Jitter acak serta pemutusan sirkuit berbasis rasio failure rate (>50%) | Mengintegrasikan konsep Jitter ke dalam draf retry dan menyusun aturan Circuit Breaker yang spesifik untuk Payment Service FoodGo |
