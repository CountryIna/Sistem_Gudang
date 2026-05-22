import random
from datetime import datetime, timedelta
from core.koneksi import konek_db

conn = konek_db()
cursor = conn.cursor()

cursor.execute("SELECT kode, harga, ukuran from barang")
list_barang = cursor.fetchall()

if not list_barang:
    print("Tabel Barang Kosong")
    exit()

jml_transaksi = 300
tgl_mulai = datetime(2026,1,1)
print("Sedang memasukkan data transaksi...")

try:
    for i in range(jml_transaksi):
        hari_acak = random.randint(0, 135)
        tgl_transaksi = tgl_mulai + timedelta(days=hari_acak)
        tgl_str = tgl_transaksi.strftime("%Y-%m-%d")

        cursor.execute("INSERT INTO transaksi(tgl, total) VALUES (%s, %s)", (tgl_str, 0))
        id_transaksi = cursor.lastrowid

        jml_barang = random.randint(1, 3)
        barang_dibeli = random.sample(list_barang, jml_barang)

        total_belanja = 0
        for barang in barang_dibeli:
            kd_barang = barang[0]
            harga_barang = int(barang[1])
            ukuran_barang = barang[2]

            if ukuran_barang in ['M', 'L']:
                qty = random.randint(1,4)
            else:
                qty = random.randint(1,2)

            subtotal = harga_barang * qty
            total_belanja += subtotal

            cursor.execute("INSERT INTO detail_transaksi (id_transaksi, kode_barang, harga, qty) VALUES (%s, %s, %s, %s)",
                           (id_transaksi, kd_barang, harga_barang, qty)
                           )

        cursor.execute("UPDATE transaksi SET total = %s WHERE id_transaksi = %s",
                        (total_belanja, id_transaksi)
                       )
    conn.commit()
    print(f"🔥 Sukses! {jml_transaksi} Transaksi Berhasil di Generate")

except Exception as e:
    conn.rollback()
    print(f"Terjadi error : {e}")

finally:
    cursor.close()
    conn.close()