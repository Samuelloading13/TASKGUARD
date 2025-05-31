import os
import csv
from datetime import datetime, timedelta

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
CSV_FILE = 'TASK.csv'

def muat_task():
    task = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline = '', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task.append(row)
    return task

def simpan_tugas(task):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['nama', 'klasifikasi', 'deadline', 'tingkat kesulitan']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(task)   

task = muat_task()

def tambah_tugas():
    print("=== Tambah Tugas ===")
    print("Ketik 'batal' kapan saja untuk membatalkan penambahan tugas\n")
    
    while True:
        nama = input("Nama Tugas: ").strip()
        if nama.lower() == 'batal':
            print("Penambahan tugas dibatalkan")
            return
        if nama == "":
            print("Nama tidak boleh kosong")
        elif nama.isdigit():
            print("Nama tidak boleh angka saja")
        else:
            break
            
    while True:
        print("\nPilihan klasifikasi: Tugas harian, UTS, UAS")
        klasifikasi = input("Klasifikasi Tugas: ").strip()
        if klasifikasi.lower() == 'batal':
            print("Penambahan tugas dibatalkan")
            return
        if klasifikasi == "":
            print("Klasifikasi tidak boleh kosong")
        elif klasifikasi.isdigit():
            print("Klasifikasi tidak boleh berupa angka")
        elif klasifikasi.lower() not in ['tugas harian', 'uts', 'uas']:
            print("Pilihan tidak valid. Harap pilih dari: Tugas harian, UTS, UAS")
        else:
            break

    while True:
        deadline = input("\nDeadline (DD-MM-YYYY): ").strip()
        if deadline.lower() == 'batal':
            print("Penambahan tugas dibatalkan")
            return
        if deadline == "":
            print("Deadline tidak boleh kosong")
            continue
        try:
            datetime.strptime(deadline, '%d-%m-%Y')
            break
        except ValueError:
            print("Format tanggal tidak valid. Gunakan DD-MM-YYYY")

    while True:
        print("\nPilihan tingkat kesulitan: mudah, sedang, susah")
        tingkat_kesulitan = input("Tingkat Kesulitan: ").strip()
        if tingkat_kesulitan.lower() == 'batal':
            print("Penambahan tugas dibatalkan")
            return
        if tingkat_kesulitan == "":
            print("Tingkat kesulitan tidak boleh kosong")
        elif tingkat_kesulitan.isdigit():
            print("Tingkat kesulitan tidak boleh berupa angka")
        elif tingkat_kesulitan.lower() not in ['mudah', 'sedang', 'susah']:
            print("Pilihan tidak valid. Harap pilih dari: mudah, sedang, susah")
        else:
            break

    print(f"\nRingkasan Tugas:")
    print(f"Nama: {nama}")
    print(f"Klasifikasi: {klasifikasi}")
    print(f"Deadline: {deadline}")
    print(f"Tingkat Kesulitan: {tingkat_kesulitan}")
    
    while True:
        konfirmasi = input("\nSimpan tugas ini? (ya/tidak): ").lower()
        if konfirmasi == 'batal' or konfirmasi == 'tidak':
            print("Penambahan tugas dibatalkan")
            return
        elif konfirmasi == 'ya':
            break
        else:
            print("Pilihan tidak valid. Ketik 'ya' atau 'tidak'")

    tugas = {
        "nama": nama,
        "klasifikasi": klasifikasi,
        "deadline": deadline,
        "tingkat kesulitan": tingkat_kesulitan
    }
    
    task.append(tugas)
    simpan_tugas(task)
    print("\n✓ Tugas berhasil ditambahkan")
    
def lihat_tugas():
    print("\nDAFTAR TUGAS")
    print("=" * 70)
    if not task:
        print("Tidak ada tugas yang tersedia")
        print("=" * 70)
        return

    print(f"{'No.':<4} | {'Nama Tugas':<20} | {'Klasifikasi':<12} | {'Deadline':<10} | {'Kesulitan':<10}")
    print("-" * 70)

    for i, tugas in enumerate(task, 1):
        nama = tugas['nama'][:18] + '..' if len(tugas['nama']) > 20 else tugas['nama']
        klasifikasi = tugas['klasifikasi'][:10] + '..' if len(tugas['klasifikasi']) > 12 else tugas['klasifikasi']
        deadline = tugas['deadline']
        kesulitan = tugas['tingkat kesulitan'][:8] + '..' if len(tugas['tingkat kesulitan']) > 10 else tugas['tingkat kesulitan']
        
        print(f"{i:<4} | {nama:<20} | {klasifikasi:<12} | {deadline:<10} | {kesulitan:<10}")
    
    print("=" * 70)

def edit_tugas():
    lihat_tugas()
    if not task:
        return
    try:
        idx =int(input("Pilih nomer tugas yg ingin di edit: "))-1
        if 0 <= idx < len(task):
            print("Kosongkan bila nilai tidak ingin diubah")
            nama = input(f"Nama: [{task[idx]['nama']}]: Nama baru: ") or task[idx]['nama']
            klasifikasi = input(f"Klasifikasi: [{task[idx]['klasifikasi']}]: Klasifikasi baru: ") or task[idx]['klasifikasi']
            deadline = input(f"Deadline: [{task[idx]['deadline']}]: Deadline baru: ") or task[idx]['deadline']
            tingkat_kesulitan = input(f"Tingkat kesulitan: [{task[idx]['tingkat kesulitan']}]: Tingkat kesulitan baru: ") or task[idx]['tingkat kesulitan']
            
            task[idx]={
                "nama": nama,
                "klasifikasi": klasifikasi,
                "deadline": deadline,
                "tingkat kesulitan": tingkat_kesulitan
                
            }

            simpan_tugas(task)
            print("Tugas Berhasil Diperbarui")
        else:
            print("Nomor Tugas Tidak Ditemukan")
    except ValueError:
        print("Input Tidak Valid")
        
def hapus_tugas():
    lihat_tugas()
    if not task:
        return
    try:
        idx = int(input("Pilih nomer tugas yg ingin dihapus: "))-1
        if 0 <= idx < len(task):
            del task[idx]
            simpan_tugas(task)
            print("Tugas Berhasil Dihapus")
        else:
            print("Nomor Tugas Tidak Ditemukan")
    except ValueError:
        print("Input Tidak Valid")
        
def submenu_pencatatan():
    while True:
        clear_screen()
        print("=== Pencatatan Tugas ===")
        print("1. Tambah Tugas")
        print("2. Lihat Tugas")
        print("3. Edit Tugas")
        print("4. Hapus Tugas")
        print("5. Kembali ke Menu Utama")
        
        pilihan = input("Pilih (1-5): ")
        
        clear_screen()
        
        if pilihan == '1':
            tambah_tugas()
        elif pilihan == '2':
            lihat_tugas()
        elif pilihan == '3':
            edit_tugas()
        elif pilihan == '4':
            hapus_tugas()
        elif pilihan == '5':
            break
        else:
            print("Input Tidak Valid")
            
        if pilihan != '5':
            input("Tekan Enter untuk melanjutkan")

def pengurutan_dan_prioritas_tugas():
    clear_screen()
    print("=== PENGURUTAN DAN PRIORITAS TUGAS ===")
    
    if not task:
        print("Tidak ada tugas yang tersedia.")
        input("\nTekan Enter untuk kembali ke menu utama...")
        return

    tugas_dengan_bobot = hitung_bobot_tugas(task)

    tugas_terurut = quick_sort_tugas(tugas_dengan_bobot)
    
    tampilkan_tugas_terurut(tugas_terurut)
    
    return

def hitung_bobot_tugas(tugas_list):
    hari_ini = datetime.now().date()
    tugas_dengan_bobot = []
    
    for tugas in tugas_list:
        try:
            deadline_date = datetime.strptime(tugas['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            
            if tugas['tingkat kesulitan'].lower() == 'susah':
                bobot_kesulitan = 3
            elif tugas['tingkat kesulitan'].lower() == 'sedang':
                bobot_kesulitan = 2
            else:
                bobot_kesulitan = 1
            
            if tugas['klasifikasi'].lower() == 'uas':
                bobot_klasifikasi = 3
            elif tugas['klasifikasi'].lower() == 'uts':
                bobot_klasifikasi = 2
            else:
                bobot_klasifikasi = 1

            if selisih_hari <= 0:
                bobot_deadline = 5
            elif selisih_hari <= 3: 
                bobot_deadline = 4
            elif selisih_hari <= 7: 
                bobot_deadline = 3
            elif selisih_hari <= 14:
                bobot_deadline = 2
            else:
                bobot_deadline = 1

            total_bobot = (bobot_kesulitan * 0.4) + (bobot_klasifikasi * 0.3) + (bobot_deadline * 0.3)

            tugas_dengan_bobot.append({
                'tugas': tugas,
                'bobot': total_bobot,
                'detail_bobot': {
                    'kesulitan': bobot_kesulitan,
                    'klasifikasi': bobot_klasifikasi,
                    'deadline': bobot_deadline
                },
                'hari_menuju_deadline': selisih_hari
            })
            
        except ValueError:
            print(f"Format deadline tidak valid untuk tugas: {tugas['nama']}")
            continue
    
    return tugas_dengan_bobot

def quick_sort_tugas(tugas_list):
    if len(tugas_list) <= 1:
        return tugas_list
    
    pivot = tugas_list[len(tugas_list) // 2]
    left = [x for x in tugas_list if x['bobot'] > pivot['bobot']]
    middle = [x for x in tugas_list if x['bobot'] == pivot['bobot']]
    right = [x for x in tugas_list if x['bobot'] < pivot['bobot']]
    
    return quick_sort_tugas(left) + middle + quick_sort_tugas(right)

def tampilkan_tugas_terurut(tugas_terurut):
    print("\nDAFTAR TUGAS BERDASARKAN PRIORITAS")
    print("=" * 105)
    print(f"{'No.':<4} | {'Nama Tugas':<25} | {'Klasifikasi':<12} | {'Deadline':<10} | {'Kesulitan':<8} | {'Hari':<6} | {'Bobot':<6} | Detail Bobot")
    print("-" * 105)
    
    for i, tugas in enumerate(tugas_terurut, 1):
        nama = (tugas['tugas']['nama'][:22] + '..') if len(tugas['tugas']['nama']) > 24 else tugas['tugas']['nama']
        klasifikasi = tugas['tugas']['klasifikasi'][:10] + ('..' if len(tugas['tugas']['klasifikasi']) > 10 else '')
        deadline = tugas['tugas']['deadline']
        kesulitan = tugas['tugas']['tingkat kesulitan'][:6]
        hari_menuju = f"{tugas['hari_menuju_deadline']}h" if tugas['hari_menuju_deadline'] >= 0 else f"-{abs(tugas['hari_menuju_deadline'])}h"
        bobot = f"{tugas['bobot']:.2f}"
        detail_bobot = f"K:{tugas['detail_bobot']['kesulitan']} T:{tugas['detail_bobot']['klasifikasi']} D:{tugas['detail_bobot']['deadline']}"
        
        print(f"{i:<4} | {nama:<25} | {klasifikasi:<12} | {deadline:<10} | {kesulitan:<8} | {hari_menuju:<6} | {bobot:<6} | {detail_bobot}")
    
    print("=" * 105)
    print("\nKETERANGAN:")
    print("Kesulitan    : (1=Mudah, 2=Sedang, 3=Susah)")
    print("Tipe         : (1=Tugas Harian, 2=UTS, 3=UAS)")
    print("Deadline     : (1=Jauh, 2=14-8h, 3=7-4h, 4=3-0h, 5=Lewat)")

def pencarian_tugas():
    while True:
        clear_screen()
        print("=== Pencarian Tugas ===")
        print("1. Cari berdasarkan Nama")
        print("2. Cari berdasarkan Klasifikasi")
        print("3. Cari berdasarkan Deadline")
        print("4. Cari berdasarkan Tingkat Kesulitan")
        print("5. Kembali ke Menu Utama")
        
        pilihan = input("Pilih jenis pencarian (1-5): ")
        
        clear_screen()
        
        if pilihan == '1':
            keyword = input("Masukkan nama tugas yang dicari: ").lower()
            hasil = [tugas for tugas in task if keyword in tugas['nama'].lower()]
            judul = f"Hasil Pencarian untuk Nama: '{keyword}'"
        elif pilihan == '2':
            print("Pilihan klasifikasi: Tugas harian, UTS, UAS")
            keyword = input("Masukkan klasifikasi tugas: ").lower()
            hasil = [tugas for tugas in task if keyword in tugas['klasifikasi'].lower()]
            judul = f"Hasil Pencarian untuk Klasifikasi: '{keyword}'"
        elif pilihan == '3':
            keyword = input("Masukkan deadline (DD-MM-YYYY atau bulan/tahun): ")
            try:
                hasil = [tugas for tugas in task if keyword in tugas['deadline']]
                if not hasil:
                    bulan_tahun = keyword.split('-')[1:] if '-' in keyword else keyword.split('/')[1:]
                    if len(bulan_tahun) >= 2:
                        hasil = [tugas for tugas in task if '-'.join(bulan_tahun) in tugas['deadline']]
                judul = f"Hasil Pencarian untuk Deadline: '{keyword}'"
            except:
                hasil = []
                judul = "Format deadline tidak valid"
        elif pilihan == '4':
            print("Pilihan: mudah, sedang, susah")
            keyword = input("Masukkan tingkat kesulitan: ").lower()
            hasil = [tugas for tugas in task if keyword in tugas['tingkat kesulitan'].lower()]
            judul = f"Hasil Pencarian untuk Tingkat Kesulitan: '{keyword}'"
        elif pilihan == '5':
            return
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")
            continue

        clear_screen()
        print(judul)
        print("-" * 50)
        if not hasil:
            print("Tidak ditemukan tugas yang sesuai!")
        else:
            for i, tugas in enumerate(hasil, 1):
                print(f"{i}. Nama: {tugas['nama']}")
                print(f"   Klasifikasi: {tugas['klasifikasi']}")
                print(f"   Deadline: {tugas['deadline']}")
                print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
                print("-" * 50)
        
        input("\nTekan Enter untuk melanjutkan...")

def pengingat_deadline():
    clear_screen()
    print("=== PENGINGAT DEADLINE ===")
    
    hari_ini = datetime.now().date()
    deadline_terdekat = []
    deadline_lewat = []
    
    for tugas in task:
        try:
            deadline_date = datetime.strptime(tugas['deadline'], '%d-%m-%Y').date()
            
            selisih_hari = (deadline_date - hari_ini).days
            
            if selisih_hari < 0:
                deadline_lewat.append((tugas, abs(selisih_hari)))
            elif 0 <= selisih_hari <= 7:
                deadline_terdekat.append((tugas, selisih_hari))
                
        except ValueError:
            print(f"Format deadline tidak valid untuk tugas: {tugas['nama']}")
            continue
    
    if deadline_lewat:
        print("\n TUGAS YANG SUDAH LEWAT DEADLINE:")
        print("=" * 50)
        for tugas, hari_lewat in sorted(deadline_lewat, key=lambda x: x[1]):
            print(f"🔴 {tugas['nama']} (Lewat {hari_lewat} hari)")
            print(f"   Deadline: {tugas['deadline']}")
            print(f"   Klasifikasi: {tugas['klasifikasi']}")
            print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
            print("-" * 50)
    else:
        print("\n Tidak ada tugas yang lewat deadline")

    if deadline_terdekat:
        print("\n TUGAS YANG MENDEKATI DEADLINE:")
        print("=" * 50)
        for tugas, hari_menuju in sorted(deadline_terdekat, key=lambda x: x[1]):
            print(f"🟡 {tugas['nama']} ({hari_menuju} hari lagi)")
            print(f"   Deadline: {tugas['deadline']}")
            print(f"   Klasifikasi: {tugas['klasifikasi']}")
            print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
            print("-" * 50)
    else:
        print("\n Tidak ada tugas yang mendekati deadline dalam 7 hari ke depan")

    tugas_jauh = [t for t in task 
                 if datetime.strptime(t['deadline'], '%d-%m-%Y').date() - hari_ini > timedelta(days=7)]
    
    if tugas_jauh:
        print("\n TUGAS DENGAN DEADLINE JAUH:")
        print("=" * 50)
        for tugas in tugas_jauh:
            deadline_date = datetime.strptime(tugas['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            print(f"🟢 {tugas['nama']} ({selisih_hari} hari lagi)")
            print(f"   Deadline: {tugas['deadline']}")
            print("-" * 50)

    return

def menu_utama():
    while True:
        clear_screen()
        print("=== MENU UTAMA TASKGUARD ===")
        print("1. Pencatatan Tugas")
        print("2. Pengurutan dan Prioritas Tugas")
        print("3. Pencarian Tugas")
        print("4. Pengingat Deadline Tugas")
        print("5. Keluar")

        pilihan = input("Pilih fitur (1-5): ")

        clear_screen()

        if pilihan == '1':
            submenu_pencatatan()
        elif pilihan == '2':
            pengurutan_dan_prioritas_tugas()
        elif pilihan == '3':
            pencarian_tugas()
        elif pilihan == '4':
            pengingat_deadline()
        elif pilihan == '5':
            print("Terima kasih telah menggunakan TASKGUARD!")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih angka 1-5.")

        if pilihan != '5':
            input("\nTekan Enter untuk kembali ke menu...")

def tampilkan_splash_screen():
    clear_screen()
    print("\n" * 5)
    print(" " * 15 + "=================================")
    print(" " * 15 + "|                               |")
    print(" " * 15 + "|           TASKGUARD           |")
    print(" " * 15 + "|    Manajemen Tugas Mahasiswa  |")
    print(" " * 15 + "|                               |")
    print(" " * 15 + "=================================")
    print("\n" * 5)
    print(" " * 17 + "Tekan Enter untuk memulai...")
    input()

tampilkan_splash_screen()
clear_screen()
menu_utama()