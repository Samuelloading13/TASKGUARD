import os
import csv
from datetime import datetime

CSV_FILE = 'TASK.csv'

def clear_screen():
    os.system('cls')

def muat_task():
    tasks = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            try:
                tasks = list(csv.DictReader(file))
            except (csv.Error, ValueError):
                print("Peringatan: File CSV korup atau tidak bisa dibaca.")
    return tasks

def simpan_tugas(tasks):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['nama', 'klasifikasi', 'deadline', 'tingkat kesulitan']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

task = muat_task()

def hitung_nilai_prioritas(tugas_list):
    hari_ini = datetime.now().date()
    tugas_bernilai = []
    bobot_map = {'kesulitan': {'susah': 3, 'sedang': 2, 'mudah': 1}, 'klasifikasi': {'uas': 3, 'uts': 2, 'tugas harian': 1}}
    for t in tugas_list:
        try:
            deadline_date = datetime.strptime(t['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            bobot_kesulitan = bobot_map['kesulitan'].get(t.get('tingkat kesulitan', '').lower(), 1)
            bobot_klasifikasi = bobot_map['klasifikasi'].get(t.get('klasifikasi', '').lower(), 1)
            if selisih_hari < 0: bobot_deadline = 5
            elif selisih_hari <= 3: bobot_deadline = 4
            elif selisih_hari <= 7: bobot_deadline = 3
            else: bobot_deadline = 1
            nilai = (bobot_kesulitan * 0.4) + (bobot_klasifikasi * 0.3) + (bobot_deadline * 0.3)
            tugas_bernilai.append({'tugas': t, 'nilai': nilai})
        except (ValueError, KeyError):
            continue
    return tugas_bernilai

def hitung_bobot_usaha(tugas):
    bobot = 0
    kesulitan_map = {'mudah': 1, 'sedang': 3, 'susah': 5}
    bobot += kesulitan_map.get(tugas.get('tingkat kesulitan', '').lower(), 1)
    klasifikasi_map = {'tugas harian': 1, 'uts': 3, 'uas': 5}
    bobot += klasifikasi_map.get(tugas.get('klasifikasi', '').lower(), 1)
    return bobot

def quick_sort_by_nilai(tugas_list):
    if len(tugas_list) <= 1:
        return tugas_list
    pivot = tugas_list[len(tugas_list) // 2]['nilai']
    kiri = [x for x in tugas_list if x['nilai'] > pivot]
    tengah = [x for x in tugas_list if x['nilai'] == pivot]
    kanan = [x for x in tugas_list if x['nilai'] < pivot]
    return quick_sort_by_nilai(kiri) + tengah + quick_sort_by_nilai(kanan)

def solve_knapsack(items, capacity):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            item_bobot = items[i-1]['bobot']
            item_nilai = items[i-1]['nilai']
            if item_bobot <= w:
                dp[i][w] = max(item_nilai + dp[i-1][w - item_bobot], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    pilihan = []
    w = capacity
    for i in range(n, 0, -1):
        if w > 0 and dp[i][w] != dp[i-1][w]:
            pilihan.append(items[i-1])
            w -= items[i-1]['bobot']
    return pilihan

def binary_search(data, target, key):
    low, high = 0, len(data) - 1
    hasil = []
    while low <= high:
        mid = (low + high) // 2
        mid_val = data[mid][key].lower()
        if mid_val == target.lower():
            hasil.append(data[mid])
            l, r = mid - 1, mid + 1
            while l >= 0 and data[l][key].lower() == target.lower():
                hasil.append(data[l]); l -= 1
            while r < len(data) and data[r][key].lower() == target.lower():
                hasil.append(data[r]); r += 1
            return hasil
        elif mid_val < target.lower():
            low = mid + 1
        else:
            high = mid - 1
    return hasil

def tambah_tugas():
    clear_screen()
    print("--- Tambah Tugas Baru ---")
    nama = input("Nama Tugas: ").strip()
    if not nama:
        print("Nama tidak boleh kosong.")
        return
    klasifikasi = input("Klasifikasi Tugas (Tugas harian, UTS, UAS): ").strip()
    while True:
        deadline_str = input("Deadline (DD-MM-YYYY): ").strip()
        try:
            deadline_obj = datetime.strptime(deadline_str, '%d-%m-%Y').date()
            if deadline_obj < datetime.now().date(): 
                print("Error: Deadline tidak boleh tanggal yang sudah lewat.")
                continue
            break
        except ValueError:
            print("Error: Format tanggal tidak valid.")
    tingkat_kesulitan = input("Tingkat Kesulitan (mudah, sedang, susah): ").strip()
    tugas_baru = {"nama": nama, "klasifikasi": klasifikasi, "deadline": deadline_str, "tingkat kesulitan": tingkat_kesulitan}
    task.append(tugas_baru)
    simpan_tugas(task)
    print("\nTugas berhasil ditambahkan!")

def edit_tugas():
    fitur_lihat_terurut_quicksort()
    if not task:
        return
    try:
        idx = int(input("\nPilih nomor tugas untuk di-edit: ")) - 1
        if 0 <= idx < len(task):
            t = task[idx]
            print("\nKosongkan jika tidak ingin diubah.")
            nama_baru = input(f"Nama [{t['nama']}]: ") or t['nama']
            klasifikasi_baru = input(f"Klasifikasi [{t['klasifikasi']}]: ") or t['klasifikasi']
            deadline_baru = input(f"Deadline [{t['deadline']}]: ") or t['deadline']
            kesulitan_baru = input(f"Tingkat Kesulitan [{t['tingkat kesulitan']}]: ") or t['tingkat kesulitan']
            task[idx] = {"nama": nama_baru, "klasifikasi": klasifikasi_baru, "deadline": deadline_baru, "tingkat kesulitan": kesulitan_baru}
            simpan_tugas(task)
            print("\nTugas berhasil diperbarui!")
        else:
            print("\nNomor tugas tidak valid.")
    except ValueError:
        print("\nInput tidak valid.")

def hapus_tugas():
    fitur_lihat_terurut_quicksort()
    if not task:
        return
    try:
        idx = int(input("\nPilih nomor tugas untuk dihapus: ")) - 1
        if 0 <= idx < len(task):
            del task[idx]
            simpan_tugas(task)
            print("\nTugas berhasil dihapus!")
        else:
            print("\nNomor tugas tidak valid.")
    except ValueError:
        print("\nInput tidak valid.")

def tampilkan_detail_tugas(tugas):
    """Fungsi pembantu untuk menampilkan detail tugas."""
    print(f"   Nama Tugas       : {tugas['nama']}")
    print(f"   Klasifikasi      : {tugas['klasifikasi']}")
    print(f"   Deadline         : {tugas['deadline']}")
    print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")

def fitur_rekomendasi_knapsack():
    clear_screen()
    print("REKOMENDASI TUGAS (KNAPSACK)")
    print("=======================================================")
    print("Fitur ini akan merekomendasikan tugas terbaik berdasarkan 'Kapasitas Poin Energi' Anda.")
    print("Setiap tugas memiliki 'Nilai Prioritas' (pentingnya) dan 'Poin Energi Dibutuhkan' (kesulitan).")
    print("\n--- PANDUAN KAPASITAS POIN ENERGI ANDA ---")
    print("  1-5 Poin   : Sedikit Energi (Cocok untuk tugas ringan)")
    print("  5-10 Poin  : Energi Sedang (Cukup untuk tugas normal)")
    print("  10-15 Poin : Energi Cukup Banyak (Bisa mengerjakan beberapa tugas penting)")
    print("  15+ Poin   : Energi Berlimpah (Siap untuk tugas-tugas besar!)")
    print("=======================================================")
    try:
        kapasitas = int(input("\nMasukkan Kapasitas Poin Energi Anda hari ini (misal: 10): "))
        if kapasitas <= 0:
            print("Kapasitas harus lebih dari 0. Mohon masukkan angka yang valid.")
            return
    except ValueError:
        print("Input tidak valid. Harap masukkan angka bulat untuk kapasitas energi Anda.")
        return

    items = []
    tugas_bernilai = hitung_nilai_prioritas(task)
    for item_berniali in tugas_bernilai:
        tugas_item = item_berniali['tugas']
        if 'tingkat kesulitan' in tugas_item and 'klasifikasi' in tugas_item:
            items.append({'nama': tugas_item['nama'],
                          'nilai': item_berniali['nilai'],
                          'bobot': hitung_bobot_usaha(tugas_item),
                          'detail': tugas_item})

    rekomendasi_terpilih = solve_knapsack(items, kapasitas)
    
    print(f"\n--- REKOMENDASI TUGAS UNTUK KAPASITAS {kapasitas} POIN ENERGI ---")
    if not rekomendasi_terpilih:
        print("Tidak ada tugas yang bisa direkomendasikan dengan kapasitas energi Anda.")
        print("Coba tingkatkan 'Kapasitas Poin Energi' Anda atau tambahkan tugas baru.")
    else:
        total_bobot = sum(item['bobot'] for item in rekomendasi_terpilih)
        total_nilai = sum(item['nilai'] for item in rekomendasi_terpilih)
        print("\nBerikut adalah tugas-tugas yang disarankan untuk Anda kerjakan:")
        print("-------------------------------------------------------------")
        for i, item in enumerate(rekomendasi_terpilih, 1):
            print(f"Tugas Rekomendasi Ke-{i}:")
            tampilkan_detail_tugas(item['detail'])
            print(f"   - Perkiraan Nilai Prioritas : {item['nilai']:.2f} (semakin tinggi, semakin penting)")
            print(f"   - Perkiraan Energi Dibutuhkan: {item['bobot']} Poin (semakin tinggi, semakin banyak usaha)")
            print("-------------------------------------------------------------")
        print(f"\nTotal Energi yang akan Anda gunakan: {total_bobot} dari {kapasitas} Poin")
        print(f"Total Prioritas yang berhasil Anda capai: {total_nilai:.2f} Poin")

def fitur_lihat_terurut_quicksort():
    clear_screen()
    print("DAFTAR TUGAS TERURUT PRIORITAS (QUICKSORT)")
    if not task:
        print("Tidak ada tugas untuk diurutkan.")
        return
    tugas_bernilai = hitung_nilai_prioritas(task)
    tugas_terurut = quick_sort_by_nilai(tugas_bernilai)
    print("-" * 70)
    print(f"{'No.':<4} | {'Nama Tugas':<25} | {'Prioritas':<10} | {'Deadline':<12}")
    print("-" * 70)
    for i, item in enumerate(tugas_terurut, 1):
        t = item['tugas']
        print(f"{i:<4} | {t['nama']:<25} | {item['nilai']:<10.2f} | {t['deadline']:<12}")
    print("-" * 70)

def fitur_pencarian_binary_search():
    clear_screen()
    print("PENCARIAN CEPAT (BINARY SEARCH)")
    print("1. Cari berdasarkan Nama\n2. Cari berdasarkan Klasifikasi")
    pilihan = input("Pilih kriteria (1-2): ")
    kriteria_map = {'1': 'nama', '2': 'klasifikasi'}
    if pilihan not in kriteria_map:
        print("Pilihan tidak valid.")
        return
    key = kriteria_map[pilihan]
    keyword = input(f"Masukkan {key} yang dicari: ").strip()
    if not keyword:
        return
    data_terurut = sorted(task, key=lambda x: x[key].lower())
    hasil = binary_search(data_terurut, keyword, key)
    clear_screen()
    print(f"Hasil Pencarian untuk '{keyword}':")
    print("-" * 70)
    if not hasil:
        print("Tidak ada tugas yang cocok ditemukan.")
    else:
        for i, t in enumerate(hasil, 1):
            print(f"{i}. {t['nama']} | {t['klasifikasi']} | {t['deadline']} | {t['tingkat kesulitan']}")
    print("-" * 70)

def bersihkan_tugas_lewat():
    clear_screen()
    print("BERSIHKAN TUGAS LEWAT DEADLINE")
    hari_ini = datetime.now().date()
    tugas_lewat = [t for t in task if datetime.strptime(t['deadline'], '%d-%m-%Y').date() < hari_ini]
    tugas_aman = [t for t in task if datetime.strptime(t['deadline'], '%d-%m-%Y').date() >= hari_ini]
    if not tugas_lewat:
        print("Tidak ada tugas yang sudah lewat deadline. Bersih!")
        return
    print("Tugas berikut sudah lewat deadline:")
    for i, t in enumerate(tugas_lewat, 1):
        print(f"{i}. {t['nama']} (Deadline: {t['deadline']})")
    konfirmasi = input(f"\nAnda yakin ingin menghapus {len(tugas_lewat)} tugas ini? (ya/tidak): ").lower()
    if konfirmasi == 'ya':
        task[:] = tugas_aman
        simpan_tugas(task)
        print(f"\n{len(tugas_lewat)} tugas berhasil dihapus.")
    else:
        print("\nPenghapusan dibatalkan.")

def tampilkan_pengingat_deadline():
    hari_ini = datetime.now().date()
    tugas_mendesak = []
    for t in task:
        try:
            selisih_hari = (datetime.strptime(t['deadline'], '%d-%m-%Y').date() - hari_ini).days
            if 0 <= selisih_hari <= 2:
                tugas_mendesak.append((t, selisih_hari))
        except (ValueError, KeyError):
            continue
    if tugas_mendesak:
        print("PENGINGAT DEADLINE")
        for t, hari in sorted(tugas_mendesak, key=lambda x: x[1]):
            pesan = "(Hari Ini!)" if hari == 0 else f"({hari} hari lagi!)"
            print(f"   - {t['nama']} {pesan}")
        print("-" * 30)

def submenu_pencatatan():
    pilihan = ''
    while pilihan != '5':
        clear_screen()
        print("--- Submenu Daftar Tugas ---")
        print("1. Tambah Tugas Baru")
        print("2. Lihat Semua Tugas (Terurut Prioritas)")
        print("3. Edit Tugas")
        print("4. Hapus Tugas")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih (1-5): ")
        if pilihan == '1':
            tambah_tugas()
        elif pilihan == '2':
            fitur_lihat_terurut_quicksort()
        elif pilihan == '3':
            edit_tugas()
        elif pilihan == '4':
            hapus_tugas()
        if pilihan in '1234':
            input("\nTekan Enter untuk melanjutkan...")

def main():
    pilihan = ''
    while pilihan != '5':
        clear_screen()
        tampilkan_pengingat_deadline()
        print("\n=== MENU UTAMA TASKGUARD ===")
        print("1. Kelola Tugas")
        print("2. Rekomendasi Tugas")
        print("3. Pencarian Cepat Tugas")
        print("4. Bersihkan Tugas yang Sudah Lewat Deadline")
        print("5. Keluar")
        pilihan = input("Pilih fitur (1-5): ")

        if pilihan == '1':
            submenu_pencatatan()
        elif pilihan == '2':
            fitur_rekomendasi_knapsack()
        elif pilihan == '3':
            fitur_pencarian_binary_search()
        elif pilihan == '4':
            bersihkan_tugas_lewat()
        elif pilihan == '5':
            print("Terima kasih telah menggunakan TASKGUARD!")
        else:
            print("Pilihan tidak valid.")
        
        if pilihan != '5':
            input("\nTekan Enter untuk kembali ke menu...")

main()