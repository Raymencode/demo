from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import random


def idenimage():
    chromedrive_path = "/Users/admin/Downloads/chromedriver"

    options = webdriver.ChromeOptions()

    options.add_argument('--start-maximized')

    rnum = random.random()

    driver = webdriver.Chrome(options=options, executable_path=chromedrive_path)

    driver.get("https://pc.zuihuibao.cn/php2/mobile/login_verify_code.php?uuid=10000500005&{}".format(rnum))

    iden_img = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body > img')))

    print(iden_img)

    driver.save_screenshot('img/capture.png')

    iden1_img = driver.find_element_by_xpath("/html/body/img")

    left = iden1_img.location['x']
    top = iden1_img.location['y']
    right = iden1_img.location['x'] + iden1_img.size['width']
    bottom = iden1_img.location['y'] + iden1_img.size['height']

    im = Image.open("img/capture.png")
    im = im.crop((left*2, top*2, right*2, bottom*2))  # 对浏览器截图进行裁剪
    im.save('img/iden.png')
    driver.quit()

    print("截图完成")


if "__name__" == "__main__":
    idenimage()
