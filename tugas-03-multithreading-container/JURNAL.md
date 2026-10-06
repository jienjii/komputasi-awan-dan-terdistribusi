# Jurnal Proses — Tugas 3

## Coba tanpa Kunci

- Hasil `processed_count` yang didapat: 36
- Kenapa bisa meleset (jelaskan mekanisme kondisi balapan dengan kata sendiri): Beberapa thread mengakses dan memperbarui variabel `processed_count` secara bersamaan tanpa sinkronisasi. Karena operasi `processed_count += 1` terdiri dari 3 tahap (baca, tambah, simpan), thread-thread membaca nilai lama yang sama sebelum thread lain sempat menyimpan nilai baru. Akibatnya, pembaruan dari beberapa thread saling menimpa dan hasil akhirnya jauh di bawah 100.

## Percobaan dengan Kunci

- Hasil `processed_count` setelah perbaikan: 100

### Perbandingan Percobaan (Tanpa Lock vs Dengan Lock)

| Parameter | Tanpa Lock (`processed_count += 1`) | Dengan Lock (`with lock:`) |
|---|---|---|
| **Hasil Akhir Counter** | 36 / 100 pesanan (Meleset) | 100 / 100 pesanan (Tepat) |
| **Status Program** | *Race Condition* Terdeteksi | Berhasil / *Thread-Safe* |
| **Mekanisme Eksekusi** | Banyak thread berebutan mengedit data di memori secara simultan. | Thread wajib mengantre; hanya 1 thread yang bisa mengedit variabel dalam satu waktu. |

## Kendala Docker

- Kesalahan yang ditemui saat `docker build` / `docker run` dan cara memperbaikinya: Bagian pengerjaan dan pengujian Docker dilakukan oleh anggota kelompok yang bertugas di bagian Docker.

## Penggunaan Log AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Alat AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah tulisan jadi/kode sendiri |
|---|---|---|---|---|
| 06-10-2026 | ChatGPT | Meminta bantuan memahami dan melengkapi Tugas 3 bagian multithreading dan race condition. | Memberikan penjelasan logika race condition serta struktur penerapan `threading.Lock()` dan pembagian worker. | Mempelajari penjelasan konsepnya, menyusun logika pembagian array ke thread, serta menambahkan block `with lock:` pada kode secara manual dan mengujinya. |
