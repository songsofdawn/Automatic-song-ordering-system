import logging
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
import os
import time
import sys

if len(sys.argv) < 2:
    print("❌ 错误：缺少歌曲名参数。请传入歌曲名称")
    sys.exit(1)

keyword = sys.argv[1]

LOGGER.setLevel(logging.WARNING)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver_path = r"C:\Users\86156\Desktop\Program\python_work\练习\chromedriver.exe"
user_data_dir = r"C:\Users\86156\AppData\Local\Google\Chrome\NewUserData"

if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)

options = webdriver.ChromeOptions()
options.binary_location = chrome_path
options.add_argument("--start-maximized")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument(r'--profile-directory=Default')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
})

try:
    encoded_keyword = quote(keyword)
    search_url = f"https://search.bilibili.com/all?keyword={encoded_keyword}"
    driver.get(search_url)

    first_video = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.bili-video-card__wrap a'))
    )

    main_window = driver.current_window_handle
    first_video.click()

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bpx-player-video-wrap video'))
    )

    driver.execute_script("""
        const video = document.querySelector('video');
        if (video) {
            video.autoplay = false;
            video.loop = false;
            video.addEventListener('ended', () => {
                window._video_ended = true;
            });
            video.play().catch(() => {});
        }
        window._video_ended = false;
    """)

    while True:
        ended = driver.execute_script("return window._video_ended === true;")
        if ended:
            break
        time.sleep(1)

except Exception as e:
    print("❌ 出现错误：", e)

finally:
    driver.quit()
    print("✅ 播放脚本已退出")
