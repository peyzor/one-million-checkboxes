import random
import time
from unittest import skip

from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from omcb import redis_connection


class ChecksSeleniumTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        cls.selenium1 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        cls.selenium2 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium1.quit()
        cls.selenium2.quit()
        super().tearDownClass()

    def scroll_to_bottom(self, driver):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")

    def test_checks(self):
        self.selenium1.get(f"{self.live_server_url}/")
        self.selenium2.get(f"{self.live_server_url}/")

        for _ in range(10):
            self.scroll_to_bottom(self.selenium1)
            self.scroll_to_bottom(self.selenium2)
            time.sleep(0.1)

        for _ in range(10):
            offset = random.randint(0, 5 * redis_connection.CHECKS_BITSET_LIMIT - 1)

            self.selenium1.find_element(By.ID, f'check-{offset}').click()
            time.sleep(0.5)

            selenium1_is_selected = self.selenium1.find_element(By.ID, f'check-{offset}').is_selected()
            selenium2_is_selected = self.selenium2.find_element(By.ID, f'check-{offset}').is_selected()
            self.assertEqual(selenium1_is_selected, selenium2_is_selected)

            self.selenium2.find_element(By.ID, f'check-{offset}').click()
            time.sleep(0.5)

            selenium1_is_selected = self.selenium1.find_element(By.ID, f'check-{offset}').is_selected()
            selenium2_is_selected = self.selenium2.find_element(By.ID, f'check-{offset}').is_selected()
            self.assertEqual(selenium1_is_selected, selenium2_is_selected)

    @skip('it is only for pleasure and must run manually')
    def test_nothing_just_go_brrr(self):
        self.selenium1.get(f"{self.live_server_url}/")
        self.selenium2.get(f"{self.live_server_url}/")

        for _ in range(20):
            self.scroll_to_bottom(self.selenium1)
            self.scroll_to_bottom(self.selenium2)
            time.sleep(0.1)

        for i in range(1000):
            offset1 = random.randint(0, 10 * redis_connection.CHECKS_BITSET_LIMIT - 1)
            offset2 = random.randint(0, 10 * redis_connection.CHECKS_BITSET_LIMIT - 1)

            try:
                self.selenium1.find_element(By.ID, f'check-{offset1}').click()
            except NoSuchElementException:
                print(f'offset: {offset1} not found')

            try:
                self.selenium2.find_element(By.ID, f'check-{offset2}').click()
            except NoSuchElementException:
                print(f'offset: {offset2} not found')
