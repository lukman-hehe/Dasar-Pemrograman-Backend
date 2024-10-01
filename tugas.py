def hitung_gaji(nama, golongan, jam_kerja):
    if golongan == 'A':
        upah_per_jam = 5000
    elif golongan == 'B':
        upah_per_jam = 7000
    elif golongan == 'C':
        upah_per_jam = 8000
    elif golongan == 'D':
        upah_per_jam = 10000
    else:
        return "Golongan tidak valid"

    if jam_kerja > 48:
        uang_lembur = (jam_kerja - 48) * 4000
    else:
        uang_lembur = 0

    upah = upah_per_jam * jam_kerja
    gaji = upah + uang_lembur

    return f"\n""## Program Python Menghitung Gaji Karyawan ##\n" \
           f"===============================================\n" \
           f"Nama Karyawan: {nama}\n" \
           f"Golongan: {golongan}\n" \
           f"Jumlah jam kerja: {jam_kerja}\n\n" \
           f"{nama} menerima upah Rp. {gaji} per minggu"

nama_karyawan = input("\n""Masukkan nama karyawan: ")
golongan_karyawan = input("Masukkan golongan karyawan (A/B/C/D): ")
jam_kerja_karyawan = int(input("Masukkan jumlah jam kerja karyawan: "))

print(hitung_gaji(nama_karyawan, golongan_karyawan, jam_kerja_karyawan))
