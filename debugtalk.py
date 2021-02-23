import time

from httprunner import __version__

import pytesseract

from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import random

def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)


def clear_image(image):
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    noise_color = get_noise_color(image)

    for x in range(width):
        for y in range(height):
            # 清除边框和干扰色
            rgb = image.getpixel((x, y))
            if (x == 0 or y == 0 or x == width - 1 or y == height - 1
                    or rgb == noise_color or rgb[1] > 100):
                image.putpixel((x, y), (255, 255, 255))
    return image


def get_noise_color(image):
    for y in range(1, image.size[1] - 1):
        # 获取第2列非白的颜色
        (r, g, b) = image.getpixel((2, y))
        if r < 255 and g < 255 and b < 255:
            return (r, g, b)


def ocrimg():

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

        driver.save_screenshot('..img/capture.png')

        iden1_img = driver.find_element_by_xpath("/html/body/img")

        left = iden1_img.location['x']
        top = iden1_img.location['y']
        right = iden1_img.location['x'] + iden1_img.size['width']
        bottom = iden1_img.location['y'] + iden1_img.size['height']

        im = Image.open("..img/capture.png")
        im = im.crop((left * 2, top * 2, right * 2, bottom * 2))  # 对浏览器截图进行裁剪
        im.save('..img/iden.png')
        driver.quit()

        print("截图完成")
        return idenimage()

    image = Image.open('..img/iden.png')
    clear_image(image)
    image = clear_image(image)
    # 转化为灰度图
    imgry = image.convert('L')
    code = pytesseract.image_to_string(imgry)
    imgry.save("..img/imgry1.png")
    print(code)
    return code


