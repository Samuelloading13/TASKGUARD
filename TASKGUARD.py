import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        print("[Pencatatan Tugas] Coming Soon...")
    elif pilihan == '2':
        print("[Pengurutan dan Prioritas Tugas] Coming Soon...")
    elif pilihan == '3':
        print("[Pencarian Tugas] Coming Soon...")
    elif pilihan == '4':
        print("[Pengingat Deadline Tugas] Coming Soon...")
    elif pilihan == '5':
        print("Terima kasih telah menggunakan TASKGUARD!")
        return
    else:
        print("Pilihan tidak valid. Silakan pilih angka 1-5.")

    input("\nTekan Enter untuk kembali ke menu...")
    menu_utama()
menu_utama()
