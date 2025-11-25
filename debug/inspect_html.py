from selenium.webdriver.common.by import By
import time
from core.driver import setup_driver
from config.routes import get_tomorrow_jakarta_yogyakarta

def debug_departing_time_structure():
    driver = setup_driver()
    url_info = get_tomorrow_jakarta_yogyakarta()

    try:
        driver.get(url_info['url'])
        time.sleep(10)

        containers = driver.find_elements(By.CSS_SELECTOR, '[data-testid="view_bus_inventory_card"]')[:2]

        for i, container in enumerate(containers):
            print(f"\nDEBUG KONTAINER {i+1}:")
            print("-" * 50)

            all_elements = container.find_elements(By.XPATH, ".//*[contains(text(), ':')]")
            time_candidates = []

            for element in all_elements:
                text = element.text.strip()
                if re.match(r'^\d{1,2}:\d{2}$', text):
                    tag = element.tag_name
                    classes = element.get_attribute("class")
                    time_candidates.append({'text': text, 'tag': tag, 'classes': classes})
                    print(f"Waktu: '{text}' | Tag: {tag}")

            if not time_candidates:
                print("Tidak ditemukan pola waktu. Cek teks manual:")
                lines = container.text.split('\n')
                for j, line in enumerate(lines, 1):
                    if ':' in line and any(c.isdigit() for c in line):
                        print(f"  Baris {j}: '{line}'")

            print("\nCoba selector eksplisit:")
            try:
                el = container.find_element(By.CSS_SELECTOR, "h4.css-4rbku5.css-901oao.r-uh8wd5.r-1b43r93.r-b88u0q.r-fdjqy7")
                print(f"Selector utama berhasil: '{el.text.strip()}'")
            except Exception as e:
                print(f"Selector utama gagal: {e}")

            h4s = container.find_elements(By.TAG_NAME, "h4")
            for idx, h4 in enumerate(h4s):
                print(f"h4[{idx}]: '{h4.text.strip()}'")

            print("-" * 50)

    finally:
        driver.quit()