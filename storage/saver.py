import pandas as pd
import datetime
import os

def save_bus_data(data, filename_prefix="nama bis"):
    if not data:
        print("Tidak ada data untuk disimpan")
        return None

    df = pd.DataFrame(data)

    column_order = [
        'platform',
        'route_name',
        'route_date',
        'route_link',
        'bus_name',
        'bus_type',
        'departing_time',
        'reaching_time',
        'duration',
        'price',
        'seat_capacity',
        'crawl_timestamp'
    ]

    available_columns = [col for col in column_order if col in df.columns]
    df_ordered = df[available_columns]

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    date_tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    excel_filename = os.path.join(output_dir, f'{filename_prefix}_{date_tomorrow}_{timestamp}.xlsx')
    csv_filename = os.path.join(output_dir, f'{filename_prefix}_{date_tomorrow}_{timestamp}.csv')

    try:
        df_ordered.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"File Excel disimpan: {excel_filename}")

        df_ordered.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"File CSV disimpan: {csv_filename}")

        print(f"Total data tersimpan: {len(df_ordered)}")
        return df_ordered

    except Exception as e:
        print(f"Gagal menyimpan file: {e}")
        return None


def print_summary(bus_data):
    if not bus_data:
        print("Tidak ada data untuk dirangkum")
        return

    print("\nProses ekstraksi selesai!")
    print(f"Jumlah bis yang berhasil diambil: {len(bus_data)}")

    if 'crawl_timestamp' in bus_data[0]:
        print(f"Waktu crawling: {bus_data[0]['crawl_timestamp']}")

    unique_companies = len(set([bus['bus_name'] for bus in bus_data]))
    print(f"Jumlah operator bis berbeda: {unique_companies}")

    departing_times = [bus['departing_time'] for bus in bus_data if bus['departing_time'] != 'Tidak diketahui']
    reaching_times = [bus['reaching_time'] for bus in bus_data if bus['reaching_time'] != 'Tidak diketahui']

    if departing_times:
        print(f"Waktu keberangkatan: {min(departing_times)} - {max(departing_times)}")
    if reaching_times:
        print(f"Waktu kedatangan: {min(reaching_times)} - {max(reaching_times)}")

    prices = [bus['price'] for bus in bus_data if bus['price'] != 'Tidak diketahui']
    if prices:
        unique_prices = sorted(set(prices))
        print(f"Kisaran harga: {unique_prices[0]} - {unique_prices[-1]}")

    durations = [bus['duration'] for bus in bus_data if bus['duration'] != 'Tidak diketahui']
    if durations:
        unique_durations = list(set(durations))[:3]
        print(f"Contoh durasi perjalanan: {', '.join(unique_durations)}")

    seat_capacities = [bus['seat_capacity'] for bus in bus_data if isinstance(bus['seat_capacity'], int)]
    if seat_capacities:
        unique_seats = sorted(set(seat_capacities))
        avg_seats = sum(seat_capacities) / len(seat_capacities)
        print(f"Kapasitas kursi tersedia: {', '.join(map(str, unique_seats))}")
        print(f"Rata-rata kapasitas: {avg_seats:.1f} kursi")

    print("\nDaftar operator bis:")
    unique_names = set([bus['bus_name'] for bus in bus_data])
    for name in sorted(unique_names):
        count = len([bus for bus in bus_data if bus['bus_name'] == name])
        print(f"  - {name} ({count} jadwal)")

    print(f"\nSumber: {bus_data[0]['platform']}")
    print(f"Rute: {bus_data[0]['route_name']}")