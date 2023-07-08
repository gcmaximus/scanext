from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the Chrome WebDriver
driver = webdriver.Chrome('/path/to/chromedriver')

# Load the Chrome extension
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('./chromedriver', options=options)

# Navigate to a web page
driver.get('file:///home/showloser/localhost/dynamic/test.html')

# # Find an input field and inject a payload
# input_element = driver.find_element_by_id('some-input-field')
# input_element.send_keys('<script>alert("XSS");</script>')

# Iterate through elements on the page and attempt to trigger events
elements = driver.find_elements(By.XPATH, '//*')
for element in elements:
    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, element.get_attribute('id'))))
        element_info = f'Tag Name: {element.tag_name}, ID: {element.get_attribute("id")}, Text: {element.text}'
        print("Attempting to trigger event on element:", element_info)
        driver.execute_script('arguments[0].click()', element)
        # break  # Exit the loop if an event is successfully triggered
    except:
        pass  # Continue iterating if an event couldn't be triggered

# Continue with other tasks or analysis
