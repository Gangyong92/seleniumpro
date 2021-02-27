from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')


class GoogleKeywordScreenshooter:

    def __init__(self, keyword, screenshoots_dir):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 브라우저 안 뜨게 하는 옵션임.
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.keyword = keyword
        self.screenshoots_dir = screenshoots_dir

    def start(self):
        self.browser.get("https://google.com")

        # 검색창 찾아서 검색어 입력 후 enter
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        try:
            # g-blk 클래스 가지는 element 찾아서 제거
            shitty_elemnet = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "g-blk")))
            self.browser.execute_script(
            """
                const shitty = arguments[0];
                shitty.parentElement.removeChild(shitty);
            """, shitty_elemnet)
        except Exception:
            # timeout시 실행 될 거임.
            pass

        # g이름을 가지는 클래스 요소들 획득
        search_results = self.browser.find_elements_by_class_name("g")

        for index, search_result in enumerate(search_results):
            search_result.screenshot(f"{self.screenshoots_dir}/{self.keyword}x{index}.png")


    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots")
domain_competitors.start()
domain_competitors.finish()

python_competitors = GoogleKeywordScreenshooter("python book", "screenshots")
python_competitors.start()
python_competitors.finish()
