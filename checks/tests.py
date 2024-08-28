import random
import time
from unittest import skip

from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from omcb import redis_connection


class ChecksSeleniumTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium1 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.selenium2 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.selenium1.implicitly_wait(3)
        cls.selenium2.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium1.quit()
        cls.selenium2.quit()
        super().tearDownClass()

    def test_checks(self):
        self.selenium1.get(f"{self.live_server_url}/")
        self.selenium2.get(f"{self.live_server_url}/")

        for _ in range(5):
            offset = random.randint(0, redis_connection.CHECKS_BITSET_LENGTH - 1)

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

        for _ in range(100):
            offset1 = random.randint(0, redis_connection.CHECKS_BITSET_LENGTH - 1)
            offset2 = random.randint(0, redis_connection.CHECKS_BITSET_LENGTH - 1)

            self.selenium1.find_element(By.ID, f'check-{offset1}').click()
            self.selenium2.find_element(By.ID, f'check-{offset2}').click()
            time.sleep(0.1)
