from math import ceil
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

BROWSER_HEIGHT = 945

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://nomadcoders.co")

# full screen으로 만들어줌. 모니터 여러개면 모든 모니터 다 사용해서 넓힘.
browser.maximize_window()

# ms에 나오는 표준 윈도우 사이즈중 가로 길이들.
sizes = [480, 960, 1366, 1920]


for size in sizes:
    browser.set_window_size(size, 1079)
    time.sleep(1)
    # scroll 사이즈 javascript로 보내고 반환 받기
    scroll_size = browser.execute_script("return document.body.scrollHeight")
    # 총 스크롤 횟수 계산
    total_sections = ceil(scroll_size / BROWSER_HEIGHT)

    # 스크롤 수행
    for section in range(total_sections + 1):
        browser.execute_script(f"window.scrollTo(0, {section * BROWSER_HEIGHT})")
        time.sleep(2)
        browser.save_screenshot(f"screenshots/{size}x{section}.png")
