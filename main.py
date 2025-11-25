from crawler.with_scroll import crawl_bus_names_with_scroll
from crawler.without_scroll import crawl_bus_names_without_scroll
from storage.saver import print_summary, save_bus_data

if __name__ == "__main__":
    print("Crawler data bis Traveloka")
    print("1. Cepat (tanpa scroll)")
    print("2. Lengkap (dengan scroll)")

    choice = input("Pilih mode (1/2): ").strip()

    if choice == "1":
        bus_data = crawl_bus_names_without_scroll()
    elif choice == "2":
        bus_data = crawl_bus_names_with_scroll()
    else:
        print("Pilihan tidak valid")
        exit()

    if bus_data:
        print_summary(bus_data)
        print("\nMenyimpan data...")
        df = save_bus_data(bus_data, "nama bis")
        if df is not None:
            print("\nSelesai. File siap digunakan.")
    else:
        print("\nTidak ada data ditemukan.")