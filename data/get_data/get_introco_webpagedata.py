from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Chrome WebDriver
service = Service("/usr/local/bin/chromedriver")  # Ensure this path is correct
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=service, options=options)

# Define URL
URL = 'https://intro.co/marketplace'

# Start the driver
driver.get(URL)

# Wait for page to load completely
wait = WebDriverWait(driver, 10)

try:
    # Wait until content is loaded (adjust the CSS selector based on inspection)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.css-selector-for-content')))

    # Infinite Scroll to Load All Data (if applicable)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new data to load
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract Data
    items = driver.find_elements(By.CSS_SELECTOR, '.your-item-class')  # Replace with the correct selector
    
    data = []
    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, '.title-class').text  # Replace with actual selector
            price = item.find_element(By.CSS_SELECTOR, '.price-class').text  # Replace with actual selector
            description = item.find_element(By.CSS_SELECTOR, '.description-class').text  # Replace with actual selector
            
            data.append({
                'Title': title,
                'Price': price,
                'Description': description
            })
        except Exception as e:
            print("Error extracting item:", e)

    # Save Data to CSV
    df = pd.DataFrame(data)
    df.to_csv('intro_marketplace_data.csv', index=False)
    print("Data saved to 'intro_marketplace_data.csv'.")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
