from math import ceil
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class ResponsiveTester:

    def __init__(self, urls):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480, 960, 1366, 1920]
        self.BROWSER_HEIGHT = 945
    
    def screenshot(self, url):
        self.browser.get(url)

        for size in self.sizes:
            self.browser.set_window_size(size, 1079)
            time.sleep(1)
            # scroll 사이즈 javascript로 보내고 반환 받기
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            # 총 스크롤 횟수 계산
            total_sections = ceil(scroll_size / self.BROWSER_HEIGHT)

            # 스크롤 수행
            for section in range(total_sections + 1):
                self.browser.execute_script(f"window.scrollTo(0, {section * self.BROWSER_HEIGHT})")
                time.sleep(2)
                self.browser.save_screenshot(f"screenshots/{size}x{section}.png")

    def start(self):
        for url in self.urls:
            self.screenshot(url)

    def finish(self):
        self.browser.quit()


tester = ResponsiveTester(["https://nomadcoders.co"])
tester.start()
tester.finish()