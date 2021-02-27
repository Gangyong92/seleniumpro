import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

def wait_for(locator):
    return WebDriverWait(browser, 10).until(EC.presence_of_element_located(locator))


main_hashtag = "dog"

browser.get("https://google.com")

# 검색창 찾아서 검색어 입력 후 enter
search_bar = browser.find_element_by_class_name("gLFyf")
search_bar.send_keys(f"#{main_hashtag} site:instagram.com +#{main_hashtag}")
search_bar.send_keys(Keys.ENTER)

"""  이미지 text가 있는 a 태그를 찾아서 반환 해줌.
 href prop 획득, 링크 이동 """ 
images = browser.find_element_by_link_text("이미지")
images.click()


# 해시태그 획득, a 태그 직접 안구하고 안에 들어가 있는 태그 획득해서 click해도 들어가짐
header = wait_for((By.CLASS_NAME, "KZ4CUc"))
hashtags = header.find_elements_by_class_name("PKhmud")

# control + click으로 각 탭으로 창을 열어줌
for hashtag in hashtags:
    ActionChains(browser).key_down(Keys.CONTROL).click(hashtag).perform()

counted_hashtags = []
used_hashtags = []

"""  browser.window_handles는 stack에 들어 가있는 것 같음. 
끝 탭에서 처음 탭으로 진행. 그리고 첫번째 탭은 제외 """
for window in browser.window_handles[1:]:
    # browser에 열려있는 각 window로 전환
    browser.switch_to_window(window)
    hashtag_name = wait_for((By.CLASS_NAME,"WTHmze"))
    print(hashtag_name.text)
    # 구글에선 해시태그 카운트가 없어서 생략
    if hashtag_name:
        if hashtag_name not in used_hashtags:
            counted_hashtags.append((hashtag_name))
            used_hashtags.append(hashtag_name)
    
# 처음에서 마지막 전 까지만 처리함.
for window in browser.window_handles[0:-1]:
    browser.switch_to_window(window)
    browser.close()



time.sleep(3)
browser.quit()