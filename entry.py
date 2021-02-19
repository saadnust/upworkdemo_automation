from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json 
import time

"""
Requirements: Chrome Webdriver (in path or in same directory)
Input: None for now
Output: Prints stocks for item and psotcode given


"""

def open_driver():
    chrome_options = Options()
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as E:
        print('Error Opening Driver')
        #send mail here
        exit(1)
    return driver

def fetch_details(driver):
    try:
        driver.get('https://www.argos.co.uk/product/6217859?clickSR=slp:term:opti%20bench:4:231:1') #for setting cookies
        driver.get("https://www.argos.co.uk/stores/api/orchestrator/v0/locator/availability?origin={}&skuQty=6217859_1".format(postcode)) #magic request
    except Exception as E:
        # send mail here
        print('Error Fetching PDP')
    try:
        js = driver.find_element_by_tag_name('pre').text
        data = json.loads(js)
    except Exception as E:
        print('Error Parsing data')
        # send mail here
        exit(1)
    return data
    

def get_stock(data):
    try:
        # loop all stores returned
        store_with_stock = []
        for each in data['stores']:
            avl = each['availability']
            for item in avl:
                #if available
                qty = item['quantityAvailable']
                if qty > 0:
                    store = avl['storeinfo']
                    store_with_stock.append({
                        'store_name':store['legacy_name'],
                        'qty_available':qty,                    
                        }) 
        return store_with_stock
    except Exception as E:
        print('Error getting stocks')
        #send mail here
        exit(1)



if __name__ == "__main__":
    #preferred using crontab/scheduler to schedule job
    postcode = 'RH10'
    while True:
        try:
            driver = open_driver()
            data = fetch_details(driver)
            stocks = get_stock(data)
            driver.quit()
            print(stocks)
        except Exception as E:
            print('Error')
            # send mail
        print('Sleeping for hour')
        time.sleep(60*60)
