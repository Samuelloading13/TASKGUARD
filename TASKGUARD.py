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
    while True:
        nama = input(("Nama Tugas: "))
        if nama =="":
            print("Nama Tidak Boleh Kosong")
        elif nama.isdigit():
            print("Nama Tidak Boleh Angka Saja")
        else:
            break
            
    while True:
        klasifikasi = input(("Klasifikasi Tugas, Pilih(Tugas harian, UTS, UAS): "))
        if klasifikasi == "":
            print("Klasifikasi Tidak Boleh Kosong")
        elif klasifikasi.isdigit():
            print("Klasifikasi Tidak Boleh Berupa Angka")
        else:
            break
    while True:
        deadline = input("Deadline Tugas, Format(DD-MM-YYYY): ")
        if deadline == "":
            print("Deadline Tidak Boleh Kosong")
            continue
        
        try:
            datetime.strptime(deadline, '%d-%m-%Y')
            break
        except ValueError:
            print("Format tanggal tidak valid. Gunakan format DD-MM-YYYY")

    while True:
        tingkat_kesulitan = input(("Tingkat Kesulitan, Pilih(mudah,sedang,susah): "))
        if tingkat_kesulitan == "":
            print("Tingkat Kesulitan Tidak Boleh Kosong")
        elif tingkat_kesulitan.isdigit():
            print("Tingkat Kesulitan Tidak Boleh Berupa Angka")
        else:
            break
    
    tugas = {
        "nama": nama,
        "klasifikasi": klasifikasi,
        "deadline": deadline,
        "tingkat kesulitan": tingkat_kesulitan
    }
    
    task.append(tugas)
    simpan_tugas(task)
    print("Tugas Berhasil Ditambahkan")
    
def lihat_tugas():
    print("=== Daftar Tugas ===")
    if not task:
        print("Tidak Ada Tugas")
        return
    for i, tugas in enumerate(task):
        print(f"{i+1}. Nama: {tugas['nama']} | Klasifikasi: {tugas['klasifikasi']} | Deadline: {tugas['deadline']} | Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
        
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
        print("5. Exit")
        
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
            return
        else:
            print("Input Tidak Valid")
            
        input("Tekan Enter untuk melanjutkan")

# def pengurutan_dan_prioritas_tugas():

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
            break
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
            # Parse tanggal deadline dari string ke objek date
            deadline_date = datetime.strptime(tugas['deadline'], '%d-%m-%Y').date()
            
            # Hitung selisih hari antara deadline dan hari ini
            selisih_hari = (deadline_date - hari_ini).days
            
            # Kategorikan tugas
            if selisih_hari < 0:
                deadline_lewat.append((tugas, abs(selisih_hari)))
            elif 0 <= selisih_hari <= 7:  # Deadline dalam 7 hari ke depan
                deadline_terdekat.append((tugas, selisih_hari))
                
        except ValueError:
            print(f"Format deadline tidak valid untuk tugas: {tugas['nama']}")
            continue
    
    # Tampilkan tugas yang sudah lewat deadline
    if deadline_lewat:
        print("\n⚠️ TUGAS YANG SUDAH LEWAT DEADLINE:")
        print("=" * 50)
        for tugas, hari_lewat in sorted(deadline_lewat, key=lambda x: x[1]):
            print(f"🔴 {tugas['nama']} (Lewat {hari_lewat} hari)")
            print(f"   Deadline: {tugas['deadline']}")
            print(f"   Klasifikasi: {tugas['klasifikasi']}")
            print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
            print("-" * 50)
    else:
        print("\n✅ Tidak ada tugas yang lewat deadline")
    
    # Tampilkan tugas yang mendekati deadline
    if deadline_terdekat:
        print("\n🔔 TUGAS YANG MENDEKATI DEADLINE:")
        print("=" * 50)
        for tugas, hari_menuju in sorted(deadline_terdekat, key=lambda x: x[1]):
            print(f"🟡 {tugas['nama']} ({hari_menuju} hari lagi)")
            print(f"   Deadline: {tugas['deadline']}")
            print(f"   Klasifikasi: {tugas['klasifikasi']}")
            print(f"   Tingkat Kesulitan: {tugas['tingkat kesulitan']}")
            print("-" * 50)
    else:
        print("\n🎉 Tidak ada tugas yang mendekati deadline dalam 7 hari ke depan")
    
    # Tampilkan tugas yang masih jauh deadline-nya
    tugas_jauh = [t for t in task 
                 if datetime.strptime(t['deadline'], '%d-%m-%Y').date() - hari_ini > timedelta(days=7)]
    
    if tugas_jauh:
        print("\n📅 TUGAS DENGAN DEADLINE JAUH:")
        print("=" * 50)
        for tugas in tugas_jauh:
            deadline_date = datetime.strptime(tugas['deadline'], '%d-%m-%Y').date()
            selisih_hari = (deadline_date - hari_ini).days
            print(f"🟢 {tugas['nama']} ({selisih_hari} hari lagi)")
            print(f"   Deadline: {tugas['deadline']}")
            print("-" * 50)
    
    input("\nTekan Enter untuk kembali ke menu utama...")
    menu_utama()

def menu_utama():
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
        print("[Pengurutan dan Prioritas Tugas] Coming Soon...")
    elif pilihan == '3':
        pencarian_tugas()
    elif pilihan == '4':
        pengingat_deadline()
    elif pilihan == '5':
        print("Terima kasih telah menggunakan TASKGUARD!")
        return
    else:
        print("Pilihan tidak valid. Silakan pilih angka 1-5.")

    input("\nTekan Enter untuk kembali ke menu...")
    menu_utama()
menu_utama()