# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat:36
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): ...

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100

## Kendala Docker
Kesalahan yang ditemui saat `docker build` / `docker run` dan cara memperbaikinya: Bagian pengerjaan dan pengujian Docker dilakukan oleh anggota kelompok yang bertugas di bagian Docker.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Alat AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah tulisan jadi/kode sendiri |
|---|---|---|---|---|
| 06-10-2026 | gemini| Meminta bantuan memahami dan melengkapi Tugas 3 bagian multithreading dan race condition. | Memberikan penjelasan logika race condition serta struktur penerapan `threading.Lock()` dan pembagian worker. | Mempelajari penjelasan konsepnya, menyusun logika pembagian array ke thread, serta menambahkan block `with lock:` pada kode secara manual dan mengujinya. |
