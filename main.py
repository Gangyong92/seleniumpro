from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://google.com")

# 검색창 찾아서 검색어 입력 후 enter
search_bar = browser.find_element_by_class_name("gLFyf")
search_bar.send_keys("hello!")
search_bar.send_keys(Keys.ENTER)

# g이름을 가지는 클래스 요소들 획득
search_results = browser.find_elements_by_class_name("g")

for search_result in search_results:
    title = search_result.find_element_by_tag_name("h3")
    if title:
        print(title.text)

# browser 종료
# browser.quit()