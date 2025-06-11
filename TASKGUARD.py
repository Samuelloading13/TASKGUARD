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
                reader = csv.DictReader(file)
                for row in reader:
                    tasks.append(row)
            except (csv.Error, ValueError):
                print("Peringatan: File CSV korup atau kosong. Membuat file baru.")
    return tasks

def simpan_tugas(tasks):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['nama', 'klasifikasi', 'deadline', 'tingkat kesulitan']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

task = muat_task()

def tambah_tugas():
    clear_screen()
    print("=== Tambah Tugas ===")
    print("Ketik 'batal' kapan saja untuk membatalkan.\n")
    
    nama = input("Nama Tugas: ").strip()
    if not nama or nama.lower() == 'batal': return

    klasifikasi = input("Klasifikasi Tugas (Tugas harian, UTS, UAS): ").strip()
    if not klasifikasi or klasifikasi.lower() == 'batal': return

    while True:
        deadline_str = input("Deadline (DD-MM-YYYY): ").strip()
        if not deadline_str or deadline_str.lower() == 'batal': return
        try:
            deadline_obj = datetime.strptime(deadline_str, '%d-%m-%Y').date()
            if deadline_obj < datetime.now().date():
                print("Error: Deadline tidak boleh tanggal yang sudah lewat. Silakan coba lagi.")
                continue
            break
        except ValueError:
            print("Error: Format tanggal tidak valid. Gunakan DD-MM-YYYY.")
    
    tingkat_kesulitan = input("Tingkat Kesulitan (mudah, sedang, susah): ").strip()
    if not tingkat_kesulitan or tingkat_kesulitan.lower() == 'batal': return
    
    tugas_baru = {"nama": nama, "klasifikasi": klasifikasi, "deadline": deadline_str, "tingkat kesulitan": tingkat_kesulitan}
    task.append(tugas_baru)
    simpan_tugas(task)
    print("\n✓ Tugas berhasil ditambahkan!")

def lihat_tugas():
    clear_screen()
    print("\nDAFTAR TUGAS")
    print("=" * 70)
    if not task:
        print("Tidak ada tugas yang tersedia.")
    else:
        print(f"{'No.':<4} | {'Nama Tugas':<20} | {'Klasifikasi':<12} | {'Deadline':<10} | {'Kesulitan':<10}")
        print("-" * 70)
        for i, t in enumerate(task, 1):
            print(f"{i:<4} | {t['nama']:<20} | {t['klasifikasi']:<12} | {t['deadline']:<10} | {t['tingkat kesulitan']:<10}")
    print("=" * 70)

def edit_tugas():
    clear_screen()
    lihat_tugas()
    if not task: return
    try:
        idx = int(input("\nPilih nomor tugas untuk di-edit: ")) - 1
        if 0 <= idx < len(task):
            print("\nKosongkan jika tidak ingin diubah.")
            t = task[idx]
            nama_baru = input(f"Nama [{t['nama']}]: ") or t['nama']
            task[idx].update({"nama": nama_baru})
            simpan_tugas(task)
            print("\n✓ Tugas berhasil diperbarui!")
        else:
            print("\nNomor tugas tidak valid.")
    except ValueError:
        print("\nInput tidak valid.")

def hapus_tugas():
    clear_screen()
    lihat_tugas()
    if not task: return
    try:
        idx = int(input("\nPilih nomor tugas untuk dihapus: ")) - 1
        if 0 <= idx < len(task):
            del task[idx]
            simpan_tugas(task)
            print("\n✓ Tugas berhasil dihapus!")
        else:
            print("\nNomor tugas tidak valid.")
    except ValueError:
        print("\nInput tidak valid.")

def hitung_nilai_prioritas(tugas_list):
    hari_ini = datetime.now().date()
    tugas_berbobot = []
    bobot_map = {'kesulitan': {'susah': 3, 'sedang': 2, 'mudah': 1}, 'klasifikasi': {'uas': 3, 'uts': 2, 'tugas harian': 1}}
    for t in tugas_list:
        try:
            deadline_date = datetime.strptime(t['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            bobot_kesulitan = bobot_map['kesulitan'].get(t['tingkat kesulitan'].lower(), 1)
            bobot_klasifikasi = bobot_map['klasifikasi'].get(t['klasifikasi'].lower(), 1)
            if selisih_hari < 0: bobot_deadline = 5
            elif selisih_hari <= 3: bobot_deadline = 4
            elif selisih_hari <= 7: bobot_deadline = 3
            else: bobot_deadline = 1
            nilai_prioritas = (bobot_kesulitan * 0.4) + (bobot_klasifikasi * 0.3) + (bobot_deadline * 0.3)
            tugas_berbobot.append({'tugas': t, 'prioritas': nilai_prioritas})
        except (ValueError, KeyError): continue
    return tugas_berbobot

def quick_sort_tugas(tugas_list):
    if len(tugas_list) <= 1: return tugas_list
    pivot = tugas_list[len(tugas_list) // 2]
    kiri = [x for x in tugas_list if x['prioritas'] > pivot['prioritas']]
    tengah = [x for x in tugas_list if x['prioritas'] == pivot['prioritas']]
    kanan = [x for x in tugas_list if x['prioritas'] < pivot['prioritas']]
    return quick_sort_tugas(kiri) + tengah + quick_sort_tugas(kanan)

def pengurutan_dan_prioritas_tugas():
    clear_screen()
    print("=== TUGAS BERDASARKAN PRIORITAS (QUICKSORT) ===")
    if not task:
        print("Tidak ada tugas untuk diurutkan.")
        return
    tugas_dengan_prioritas = hitung_nilai_prioritas(task)
    tugas_terurut = quick_sort_tugas(tugas_dengan_prioritas)
    print("-" * 60)
    for i, item in enumerate(tugas_terurut, 1):
        t = item['tugas']
        print(f"{i}. {t['nama']} (Prioritas: {item['prioritas']:.2f})")
        print(f"   Deadline: {t['deadline']} | Kesulitan: {t['tingkat kesulitan']}")
    print("-" * 60)

def binary_search(data, target, key):
    low, high = 0, len(data) - 1
    hasil = []
    while low <= high:
        mid = (low + high) // 2
        mid_val = data[mid][key].lower()
        if mid_val == target.lower():
            hasil.append(data[mid])
            l, r = mid - 1, mid + 1
            while l >= 0 and data[l][key].lower() == target.lower(): hasil.append(data[l]); l -= 1
            while r < len(data) and data[r][key].lower() == target.lower(): hasil.append(data[r]); r += 1
            return hasil
        elif mid_val < target.lower(): low = mid + 1
        else: high = mid - 1
    return hasil

def pencarian_tugas():
    clear_screen()
    print("=== PENCARIAN TUGAS (BINARY SEARCH) ===")
    print("1. Cari berdasarkan Nama\n2. Cari berdasarkan Klasifikasi\n3. Cari berdasarkan Tingkat Kesulitan")
    pilihan = input("Pilih kriteria (1-3): ")
    kriteria_map = {'1': 'nama', '2': 'klasifikasi', '3': 'tingkat kesulitan'}
    if pilihan not in kriteria_map:
        print("Pilihan tidak valid."); return
    key = kriteria_map[pilihan]
    keyword = input(f"Masukkan {key} yang dicari: ").strip()
    if not keyword: return
    data_terurut = sorted(task, key=lambda x: x[key].lower())
    hasil = binary_search(data_terurut, keyword, key)
    clear_screen()
    print(f"Hasil Pencarian untuk '{keyword}':")
    print("-" * 50)
    if not hasil:
        print("Tidak ada tugas yang cocok ditemukan.")
    else:
        for i, t in enumerate(hasil, 1):
            print(f"{i}. {t['nama']} | {t['klasifikasi']} | {t['deadline']} | {t['tingkat kesulitan']}")
    print("-" * 50)


def tampilkan_pengingat_deadline():
    hari_ini = datetime.now().date()
    batas_hari = 2
    tugas_mendesak = []
    for t in task:
        try:
            deadline_date = datetime.strptime(t['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            if 0 <= selisih_hari <= batas_hari:
                tugas_mendesak.append((t, selisih_hari))
        except (ValueError, KeyError): continue
    if tugas_mendesak:
        print("🔔 PENGINGAT DEADLINE 🔔")
        print("-" * 30)
        for t, hari in sorted(tugas_mendesak, key=lambda x: x[1]):
            if hari == 0: pesan = "(Hari Ini!)"
            elif hari == 1: pesan = "(Besok!)"
            else: pesan = f"({hari} hari lagi)"
            print(f"🟡 {t['nama']} {pesan}")
        print("-" * 30)
        print()

def bersihkan_tugas_lewat():
    clear_screen()
    print("=== BERSIHKAN TUGAS LEWAT DEADLINE ===")
    hari_ini = datetime.now().date()
    tugas_lewat = []
    tugas_aman = []

    for t in task:
        try:
            deadline_obj = datetime.strptime(t['deadline'], '%d-%m-%Y').date()
            if deadline_obj < hari_ini:
                tugas_lewat.append(t)
            else:
                tugas_aman.append(t)
        except (ValueError, KeyError):
            tugas_aman.append(t)

    if not tugas_lewat:
        print("Tidak ada tugas yang sudah lewat deadline. Bersih!")
        return

    print("Tugas berikut sudah lewat deadline:")
    for i, t in enumerate(tugas_lewat, 1):
        print(f"{i}. {t['nama']} (Deadline: {t['deadline']})")
    
    konfirmasi = input(f"\nAnda yakin ingin menghapus {len(tugas_lewat)} tugas ini secara permanen? (ya/tidak): ").lower()
    if konfirmasi == 'ya':
        task[:] = tugas_aman
        simpan_tugas(task)
        print(f"\n✓ {len(tugas_lewat)} tugas berhasil dihapus.")
    else:
        print("\nPenghapusan dibatalkan.")

def submenu_pencatatan():
    pilihan = ''
    while pilihan != '5':
        clear_screen()
        print("=== Pencatatan Tugas ===")
        print("1. Tambah Tugas\n2. Lihat Tugas\n3. Edit Tugas\n4. Hapus Tugas\n5. Kembali")
        pilihan = input("Pilih (1-5): ")
        if pilihan == '1': tambah_tugas()
        elif pilihan == '2': lihat_tugas()
        elif pilihan == '3': edit_tugas()
        elif pilihan == '4': hapus_tugas()
        if pilihan in '1234': input("\nTekan Enter untuk melanjutkan...")

def main():
    pilihan = ''
    while pilihan != '5':
        clear_screen()
        tampilkan_pengingat_deadline()
        print("=== MENU UTAMA TASKGUARD ===")
        print("1. Pencatatan Tugas")
        print("2. Prioritas & Pengurutan Tugas")
        print("3. Pencarian Tugas")
        print("4. Bersihkan Tugas Lewat Deadline")
        print("5. Keluar")
        pilihan = input("Pilih fitur (1-5): ")

        if pilihan == '1': submenu_pencatatan()
        elif pilihan == '2': pengurutan_dan_prioritas_tugas()
        elif pilihan == '3': pencarian_tugas()
        elif pilihan == '4': bersihkan_tugas_lewat()
        elif pilihan == '5': print("Terima kasih!")
        else: print("Pilihan tidak valid.")
        
        if pilihan != '5': input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()