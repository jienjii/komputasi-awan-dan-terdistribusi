"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time

NUM_ORDERS = 100
NUM_WORKERS = 10

# Counter bersama
processed_count = 0

# Lock untuk melindungi counter
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan."""
    global processed_count

    # Simulasi proses pesanan
    time.sleep(random.uniform(0.001, 0.01))

    # Counter dilindungi oleh Lock
    with lock:
        processed_count += 1


def worker(order_ids: list) -> None:
    """Thread pekerja memproses sekumpulan pesanan."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # Membagi pesanan ke beberapa thread
    chunk_size = len(order_ids) // NUM_WORKERS

    threads = []

    for i in range(NUM_WORKERS):
        start = i * chunk_size

        if i == NUM_WORKERS - 1:
            end = len(order_ids)
        else:
            end = start + chunk_size

        worker_orders = order_ids[start:end]

        thread = threading.Thread(
            target=worker,
            args=(worker_orders,)
        )

        threads.append(thread)

    # Menjalankan semua thread
    for thread in threads:
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

    print(
        f"Total pesanan diproses: "
        f"{processed_count} (seharusnya {NUM_ORDERS})"
    )

    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI!")
    else:
        print("Semua pesanan berhasil diproses dengan aman.")


if __name__ == "__main__":
    main()
