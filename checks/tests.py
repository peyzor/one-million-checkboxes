import random
import time
from omcb import redis_connection

from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class ChecksSeleniumTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_checks(self):
        self.selenium.get(f"{self.live_server_url}/")
        for _ in range(100):
            offset = random.randint(0, redis_connection.CHECKS_BITSET_LENGTH - 1)
            checkbox = self.selenium.find_element(By.ID, f'check-{offset}')
            checkbox.click()
            time.sleep(0.1)
