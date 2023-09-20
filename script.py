import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get("https://www.keldelice.com/guide/france/producteurs")
total_pages = 50
# [csv output file creation]
csv_filename = 'data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Entreprise', 'Téléphone', 'Contact', 'Addresse']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_writer.writeheader()

# [loop to get all the infos of the sellers]
for page in range(1, total_pages + 1):
    cards = driver.find_elements(By.CSS_SELECTOR, ".organization.picname")
    for card_index, card in enumerate(cards):
        select_cards = driver.find_elements(By.CSS_SELECTOR, ".organization.picname")
        print("IN CARD: ", card_index)
        select_cards[card_index].click()
        time.sleep(1)
        seller_name = driver.find_element(By.CSS_SELECTOR, ".content h2").text
        street_address = driver.find_element(By.CSS_SELECTOR, '[itemprop="street-address"]').text
        locality = driver.find_element(By.CSS_SELECTOR, '[itemprop="locality"]').text
        postal_code = driver.find_element(By.CSS_SELECTOR, '[itemprop="postal-code"]').text
        region = driver.find_element(By.CSS_SELECTOR, '[itemprop="region"]').text
        try: tel = driver.find_element(By.CSS_SELECTOR, '[itemprop="tel"]').text
        except NoSuchElementException: tel = ""
        # [write data collected in the csv output file]
        data_dict = { 'Entreprise': seller_name, 'Téléphone': tel, 'Addresse': locality + ", " + postal_code }
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writerow(data_dict)
        driver.back()
        time.sleep(1)
    print("SWITCHING PAGE")
    next = driver.find_element(By.CSS_SELECTOR, ".next_page")
    next.click()
    time.sleep(2)
driver.quit()
