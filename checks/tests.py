import random

from django.test import TestCase

from channels.testing import ChannelsLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class ChecksSeleniumTests(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/")
        for _ in range(10):
            offset = random.randint(0, 1000)
            box = self.selenium.find_element(By.ID, f'check-{offset}')
            box.click()

        print()
