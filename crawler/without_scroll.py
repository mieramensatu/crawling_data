import time
import random
import datetime
from selenium.webdriver.common.by import By
from core.driver import setup_driver
from core.extractor import (
    extract_bus_name_only,
    extract_bus_type,
    extract_departing_time,
    extract_reaching_time,
    extract_duration,
    extract_price,
    extract_seat_capacity_with_click
)
from config.routes import get_tomorrow_jakarta_yogyakarta

def crawl_bus_names_without_scroll():
    print("Mulai crawling data bis tanpa scroll")
    driver = setup_driver()
    url_info = get_tomorrow_jakarta_yogyakarta()
    bus_data = []

    try:
        print(f"Buka URL: {url_info['url']}")
        driver.get(url_info['url'])
        print("Tunggu halaman dimuat...")
        time.sleep(10)

        containers = driver.find_elements(By.CSS_SELECTOR, '[data-testid="view_bus_inventory_card"]')
        print(f"\nDitemukan {len(containers)} kontainer bis")

        crawl_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for i, container in enumerate(containers):
            print(f"Proses bis ke-{i+1} dari {len(containers)}")

            bus_name = extract_bus_name_only(container)
            bus_type = extract_bus_type(container)
            departing_time = extract_departing_time(container)
            reaching_time = extract_reaching_time(container)
            duration = extract_duration(container)
            price = extract_price(container)
            seat_capacity = extract_seat_capacity_with_click(container, driver)

            bus_data.append({
                'platform': 'Traveloka',
                'route_name': url_info['route'],
                'route_date': url_info['date'],
                'route_link': driver.current_url,
                'bus_name': bus_name,
                'bus_type': bus_type,
                'departing_time': departing_time,
                'reaching_time': reaching_time,
                'duration': duration,
                'price': price,
                'seat_capacity': seat_capacity,
                'crawl_timestamp': crawl_timestamp
            })

            print(f"Bis {i+1}: {bus_name} | Berangkat: {departing_time} | Kursi: {seat_capacity} | Harga: {price}")
            time.sleep(random.uniform(2, 4))

        return bus_data

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return []
    finally:
        driver.quit()