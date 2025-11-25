import time
import random
from selenium.webdriver.common.by import By

def smooth_auto_scroll(driver):
    print("Mulai scroll otomatis dari atas ke bawah...")

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    scroll_attempts = 0
    max_attempts = 100

    print(f"Tinggi halaman awal: {last_height} piksel")
    print("Lanjut scroll...")

    while scroll_attempts < max_attempts:
        scroll_increment = random.randint(200, 400)
        current_position += scroll_increment

        if current_position >= last_height:
            current_position = last_height
            print("Sampai di bawah halaman")

        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(0.5, 1.2))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= last_height:
            if new_height > last_height:
                print(f"Konten baru muncul. Tinggi berubah jadi {new_height} piksel")
                last_height = new_height
                scroll_attempts = 0
            else:
                print("Tidak ada konten baru. Scroll selesai.")
                break

        scroll_attempts += 1

        if scroll_attempts % 10 == 0:
            progress = (current_position / last_height) * 100
            print(f"Progres scroll: {progress:.1f}%")

    print("Tunggu sebentar...")
    time.sleep(3)

    print("Kembali ke atas...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    final_containers = driver.find_elements(By.CSS_SELECTOR, '[data-testid="view_bus_inventory_card"]')
    print(f"Ditemukan {len(final_containers)} data bis")
    return final_containers