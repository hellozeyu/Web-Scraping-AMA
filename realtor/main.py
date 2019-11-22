from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

driver = webdriver.Chrome()
# 4 example regeions but you can find the pattern and add it to the list
locations = ['Jersey-City_NJ', 'Queens_NY', 'Manhattan_NY', 'Brooklyn_NY']

for location in locations:
    driver.get('https://www.realtor.com/realestateandhomes-search/' + location)
    csv_file = open(location + '.csv', 'w', encoding='utf-8', newline='')
    items = ['property','bed', 'bath', 'sqft', 'price']
    writer = csv.writer(csv_file, items)
    # keep pressing the next button until it is not clickable
    while True:
        try:
            # wait for all the listings to be present on the page
            listings = WebDriverWait(driver, 10).until(
                       EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="srp-list-marginless list-unstyled prop-list"]/li')))
            # iterate through all the listings 
            for listing in listings:
                listing_dict = {}
                try:
                    # property is a built-in function in Python, adding _ for name mangling
                    property_ = listing.find_element_by_xpath('.//div[@class="property-type"]').text
                    listing_dict['property']= property_
                except:
                    listing_dict['property']= None

                try:
                    bed = listing.find_element_by_xpath('.//span[@class="data-value meta-beds"]').text
                    listing_dict['bed'] = bed
                except:
                    listing_dict['bed'] = None

                try:
                    bath = listing.find_element_by_xpath('.//li[@data-label="property-meta-baths"]/span').text
                    listing_dict['bath'] = bath
                except:
                    listing_dict['bath'] = None

                try:
                    # clean the format of sqft, remove the ',' from the string
                    sqft = listing.find_element_by_xpath('.//li[@data-label="property-meta-sqft" \
                                                        or @data-label="property-meta-lotsize"]/span').text
                    sqft = ''.join(sqft.split(','))
                    listing_dict['sqft'] = sqft
                except:
                    listing_dict['sqft'] = None

                try:
                    # clean the format of price, remove the '$' and ',' from the string
                    price = listing.find_element_by_xpath('.//span[@class="data-price"]').text.replace('$', '')
                    price = ''.join(price.split(','))
                    listing_dict['price'] = price
                except:
                    listing_dict['price'] = None
                # skip the listing if all the items are empty i.e ads
                if not any(listing_dict.values()):
                    continue
                writer.writerow(listing_dict.values())
            # wait for the next page button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                          EC.element_to_be_clickable((By.XPATH, '//a[@class="next"]')))
            ActionChains(driver).move_to_element(next_button).perform()
            next_button.click()
            # clear the cookies after entering a new page
            driver.delete_all_cookies()
            # sacrifice some efficiency to make sure we won't get banned 
            time.sleep(5)
        except Exception as e:
            # finished one region
            break
    csv_file.close()
driver.close()