import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_data_with_selenium(file_path, datacenter, prefix):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up the WebDriver
    service = Service('path/to/chromedriver')  # Update the path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Load the HTML file
        driver.get(f'file://{file_path}')

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "td"))
        )

        # Get the page source after rendering
        content = driver.page_source

        # Match the required HTML pattern
        matches = re.finditer(
            r"<td>\s*<img.*?>\s*<a href='([^']+)'>((\d{5})_([a-zA-Z0-9_]+)_([tsTS]\d{2,6})_.*?)</a>\s*</td>",
            content
        )

        data = []
        for match in matches:
            link_suffix = match.group(1)
            full_string = match.group(2)
            site_id = match.group(3)
            location_name = match.group(4)
            terminal = match.group(5)
            link = prefix + link_suffix

            data.append([datacenter, location_name, site_id, terminal, link])

    finally:
        driver.quit()
    
    return data

def write_to_csv(data, output_file):
    headers = ["Datacenter", "Location name", "Site ID", "Terminal", "Link Description"]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    # File paths and prefixes
    at_file = "at.html"
    mi_file = "mi.html"
    at_prefix = "https://at-orionpoll01.corp.securustech.net"
    mi_prefix = "https://mi-orionpoll01.corp.securustech.net"
    
    # Extract data from both files
    at_data = extract_data_with_selenium(at_file, "at", at_prefix)
    mi_data = extract_data_with_selenium(mi_file, "mi", mi_prefix)
    
    # Combine and write to CSV
    combined_data = at_data + mi_data
    write_to_csv(combined_data, "TerminalsOrion.csv")

if __name__ == "__main__":
    main()