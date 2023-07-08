import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class WebsiteTestCase(unittest.TestCase):

    def setUp(self):
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome()

    def test_page_title_and_element_presence(self):
        # Navigate to the website
        self.driver.get("file:///home/showloser/localhost/dynamic/test.html")

        # Check the page title
        expected_title = "Xss Website"
        actual_title = self.driver.title
        self.assertEqual(actual_title, expected_title, f"Page title mismatch. Expected: {expected_title}, Actual: {actual_title}")

        # Check the presence of the <p> element with id 'TEST'
        try:
            p_element = self.driver.find_element(By.ID, "TEST")
            is_p_present = True
        except NoSuchElementException:
            is_p_present = False

        # Assert that the <p> element with id 'TEST' is present
        self.assertTrue(is_p_present, "Element <p> with id 'TEST' is not present on the website.")

        # Check the presence of the <a> element
        try:
            a_element = self.driver.find_element(By.TAG_NAME, "a")
            is_a_present = True
        except NoSuchElementException:
            is_a_present = False

        # Assert that the <a> element is present
        self.assertTrue(is_a_present, "Element <a> is not present on the website.")

        # Check the presence of the <img> element
        try:
            img_element = self.driver.find_element(By.TAG_NAME, "img")
            is_img_present = True
        except NoSuchElementException:
            is_img_present = False

        # Assert that the <img> element is present
        self.assertTrue(is_img_present, "Element <img> is not present on the website.")

        # Check the presence of the <iframe> element
        try:
            iframe_element = self.driver.find_element(By.TAG_NAME, "iframe")
            is_iframe_present = True
        except NoSuchElementException:
            is_iframe_present = False

        # Assert that the <iframe> element is present
        self.assertTrue(is_iframe_present, "Element <iframe> is not present on the website.")

        # Check the presence of the <div> element with id 'pageUrl'
        try:
            div_element = self.driver.find_element(By.ID, "pageUrl")
            is_div_present = True
        except NoSuchElementException:
            is_div_present = False

        # Assert that the <div> element with id 'pageUrl' is present
        self.assertTrue(is_div_present, "Element <div> with id 'pageUrl' is not present on the website.")

    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
