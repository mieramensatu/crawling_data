import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def extract_bus_name_only(container):
    try:
        bus_name_element = container.find_element(By.CSS_SELECTOR, "h3.css-4rbku5.css-901oao.r-uh8wd5.r-ubezar.r-b88u0q.r-rjixqe.r-fdjqy7")
        return bus_name_element.text.strip()
    except Exception:
        return "Tidak diketahui"

def extract_bus_type(container):
    try:
        bus_type_elements = container.find_elements(By.CSS_SELECTOR, "div.css-901oao.r-uh8wd5.r-majxgm.r-fdjqy7:not(.css-bfa6kz)")
        for element in bus_type_elements:
            text = element.text.strip()
            if text and text != "Bisa Reschedule":
                return text

        all_elements = container.find_elements(By.CSS_SELECTOR, "div.css-901oao.r-uh8wd5.r-majxgm.r-fdjqy7")
        for element in all_elements:
            classes = element.get_attribute("class")
            text = element.text.strip()
            if "css-bfa6kz" not in classes and "r-jwli3a" not in classes and text and text != "Bisa Reschedule":
                return text

        return "Tidak diketahui"
    except Exception:
        return "Tidak diketahui"

def extract_departing_time(container):
    try:
        time_elements = container.find_elements(By.CSS_SELECTOR, "h4.css-4rbku5.css-901oao.r-uh8wd5.r-1b43r93.r-b88u0q.r-fdjqy7")
        time_candidates = []
        for element in time_elements:
            text = element.text.strip()
            if re.match(r'^\d{1,2}:\d{2}$', text):
                time_candidates.append(text)
        return time_candidates[0] if time_candidates else "Tidak diketahui"
    except Exception:
        return "Tidak diketahui"

def extract_reaching_time(container):
    try:
        time_elements = container.find_elements(By.CSS_SELECTOR, "h4.css-4rbku5.css-901oao.r-uh8wd5.r-1b43r93.r-b88u0q.r-fdjqy7")
        time_candidates = []
        for element in time_elements:
            text = element.text.strip()
            if re.match(r'^\d{1,2}:\d{2}$', text):
                time_candidates.append(text)
        return time_candidates[1] if len(time_candidates) >= 2 else "Tidak diketahui"
    except Exception:
        return "Tidak diketahui"

def extract_duration(container):
    try:
        duration_element = container.find_element(By.CSS_SELECTOR, "h4.css-4rbku5.css-901oao.r-uh8wd5.r-1b43r93.r-b88u0q.r-q4m81j")
        return duration_element.text.strip()
    except Exception:
        return "Tidak diketahui"

def extract_price(container):
    try:
        price_elements = container.find_elements(By.XPATH, ".//*[contains(text(), 'Rp')]")
        for element in price_elements:
            text = element.text.strip()
            if 'Rp' in text:
                price_text = re.search(r'Rp\s*[\d.,]+', text)
                if price_text:
                    return price_text.group()
        return "Tidak diketahui"
    except Exception:
        return "Tidak diketahui"

def extract_seat_capacity_with_click(container, driver):
    print("Membuka detail bis untuk cek kapasitas kursi...")

    try:
        container.click()
        time.sleep(3)
    except Exception as e:
        print(f"Gagal klik detail: {e}")
        close_modal(driver)
        return "Tidak diketahui"

    seat_capacity = "Tidak diketahui"

    try:
        seat_elements = driver.find_elements(By.CSS_SELECTOR, "span.css-901oao.css-16my406.r-uh8wd5.r-1b43r93.r-majxgm.r-rjixqe.r-fdjqy7")
        for element in seat_elements:
            text = element.text.strip()
            if 'kursi' in text.lower():
                capacity_match = re.search(r'(\d+)\s*kursi', text)
                if capacity_match:
                    seat_capacity = int(capacity_match.group(1))
                    print(f"Kapasitas kursi: {seat_capacity}")
                    break
    except Exception as e:
        print(f"Gagal baca kapasitas dari elemen spesifik: {e}")

    if seat_capacity == "Tidak diketahui":
        modal_selectors = [
            "[data-testid='bus-detail-modal']",
            ".modal-content",
            "[role='dialog']",
            ".css-1dbjc4n.r-1awozwy"
        ]
        for selector in modal_selectors:
            try:
                modal = driver.find_element(By.CSS_SELECTOR, selector)
                modal_text = modal.text
                capacity_match = re.search(r'(\d+)\s*kursi', modal_text)
                if capacity_match:
                    seat_capacity = int(capacity_match.group(1))
                    print(f"Kapasitas kursi ditemukan di teks modal: {seat_capacity}")
                    break
            except:
                continue

    close_modal(driver)
    return seat_capacity

def close_modal(driver):
    close_buttons = [
        "[data-testid='modal-close-btn']",
        ".close",
        "[aria-label='Close']",
        "button[class*='close']",
        "div[class*='close']"
    ]

    for selector in close_buttons:
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, selector)
            close_btn.click()
            time.sleep(1)
            print("Modal ditutup via tombol")
            return
        except:
            continue

    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
        time.sleep(1)
        print("Modal ditutup via tombol ESC")
    except Exception as e:
        print(f"Gagal menutup modal: {e}")