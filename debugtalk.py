import time

from httprunner import __version__

import pytesseract

from PIL import Image

import demo.identify


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
    identify()
    image = Image.open('img/iden.png')
    clear_image(image)
    image = clear_image(image)
    # 转化为灰度图
    imgry = image.convert('L')
    code = pytesseract.image_to_string(imgry)
    imgry.save("img/imgry1.png")
    print(code)
    return code


