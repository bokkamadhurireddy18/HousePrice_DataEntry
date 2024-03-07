import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sheet_url="https://docs.google.com/forms/d/e/1FAIpQLSciNn6taNnbvuJaTmj54BoduFBX9ml76IyumJV5zlVT71Dd0w/viewform?usp=sf_link"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Use our Zillow-Clone website (instead of Zillow.com)
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)

soup= BeautifulSoup(response.text, "html.parser")
price_tag = soup.select("#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper > div.StyledPropertyCardDataArea-fDSTNn > div > span")
price_list=[prices.text.strip("/mo+ 1 bd") for prices in price_tag]
print(len(price_list))

address_tag=soup.find_all("address", attrs={"data-test": "property-card-addr"})
address_list=[address.text.strip().replace('| ', '') for address in address_tag]
print(len(address_list))

address_link_tag= soup.find_all("a", attrs={"class": "property-card-link"})
address_links_list=[address_link["href"] for address_link in address_link_tag]
print(len(address_links_list))

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create and configure the Chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the google sheet
for index in range(len(address_list)):
    driver.get(sheet_url)
    time.sleep(2)

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    # Fill out the form
    address.send_keys(address_list[index])
    price.send_keys(price_list[index])
    link.send_keys(address_links_list[index])

    # Locate the "Sign Up" button. Then click on it
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()


