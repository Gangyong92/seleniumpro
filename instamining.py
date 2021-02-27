import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class Instaminer:
    def __init__(self, initial_hashtags, max_hashtags):
        self.initial_hashtags = initial_hashtags
        self.max_hashtags = max_hashtags
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.counted_hashtags = []
        self.used_hashtags = []

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(locator))
        
    def extract_data(self):
        hashtag_name = self.wait_for((By.CLASS_NAME, "WTHmze"))
        if hashtag_name:
            hashtag_name = hashtag_name.text
        # 구글에선 해시태그 카운트가 없어서 생략
        if hashtag_name:
            if hashtag_name not in self.used_hashtags:
                # count 값은 그냥 20으로 고정
                self.counted_hashtags.append((hashtag_name, 20))
                self.used_hashtags.append(hashtag_name)

    def save_file(self):
        file = open(f"{self.initial_hashtags}-report.csv", "w")
        writer = csv.writer(file)
        # column 명 지정
        writer.writerow(["Hashtag", "Post Count"])

        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

        file.close()

    def start(self):
        self.get_related(self.initial_hashtags)
    
    def get_related(self, target_hashtag):
        self.browser.get("https://google.com")

        # 검색창 찾아서 검색어 입력 후 enter
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(f"#{target_hashtag} site:instagram.com +#{target_hashtag}")
        search_bar.send_keys(Keys.ENTER)

        """  이미지 text가 있는 a 태그를 찾아서 반환 해줌.
        href prop 획득, 링크 이동 """ 
        images = self.browser.find_element_by_link_text("이미지")
        images.click()
        
        # 해시태그 획득, a 태그 직접 안구하고 안에 들어가 있는 태그 획득해서 click해도 들어가짐
        header = self.wait_for((By.CLASS_NAME, "KZ4CUc"))
        hashtags = header.find_elements_by_class_name("PKhmud")

        # control + click으로 각 탭으로 창을 열어줌
        for hashtag in hashtags:
            hashtag_name = hashtag.text
            # used_hashtags 목록에 없는 경우에만 해당 해시태그 탭을 열어 줄 거임.
            if hashtag_name not in self.used_hashtags:
                ActionChains(self.browser).key_down(Keys.CONTROL).click(hashtag).perform()

        """  browser.window_handles는 stack에 들어 가있는 것 같음. 
        끝 탭에서 처음 탭으로 진행. 그리고 첫번째 탭은 제외 """
        for window in self.browser.window_handles[1:]:
            # browser에 열려있는 각 window로 전환
            self.browser.switch_to_window(window)
            self.extract_data()

        """ 검색한 hashtag 개수가 max_hashtags 보다 적을 때만 다음을 위해 한 개의
            탭을 남길 거임. """
        if len(self.used_hashtags) < self.max_hashtags:
            # 처음에서 마지막 전 까지만 처리함.
            for window in self.browser.window_handles[0:-1]:
                self.browser.switch_to_window(window)
                self.browser.close()
            """  닫고 나서 끝이 아니라 작업할 window로 switch 시켜줘야함. 눈에는 
            마지막창이 남아 있겠지만 내부에서는 그렇지 않음.  """
            self.browser.switch_to_window(self.browser.window_handles[0])
        else:
            self.browser.quit()
            self.save_file()


Instaminer("dog", 1).start()