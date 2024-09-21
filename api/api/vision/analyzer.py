import math
import os
import urllib.request

import numpy as np
import cv2
import random

from agroboost.settings import BASE_DIR
from django.contrib.staticfiles.templatetags.staticfiles import static

boundaries = [
    ([0, 0, 0], [110, 130, 90]),
]


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def treePer(img):
    shape = img.shape

    white = 0

    for x in range(shape[0]):
        for y in range(shape[1]):
            if img[x, y] == 255:
                white += 1

    return white * 100 / (shape[0] * shape[1])


def check_green(img):
    shape = img.shape

    for x in range(shape[0]):
        for y in range(shape[1]):
            r, g, b = img[x, y]

            if g < r and g < b:
                img[x, y] = [0, 0, 0]

            if g + 10 < r or g + 10 < b:
                img[x, y] = [0, 0, 0]

    return img


def analyze(x, y, z):
    path = "http://{}.google.com/vt/lyrs=s&x={}&y={}&z={}".format(
        ['mt0', 'mt1', 'mt2', 'mt3'][random.randint(0, 3)], x, y, z)
    image = url_to_image(path)

    source_file = (BASE_DIR + '/images/source/{}/{}/{}').format(z, x, y)
    analyzed_file = (BASE_DIR + '/images/analyzed/{}/{}/{}').format(z, x, y)
    perc_file = analyzed_file + '/perc.txt'

    os.makedirs(source_file, exist_ok=True)
    os.makedirs(analyzed_file, exist_ok=True)

    if (os.path.isfile(perc_file)):
        with open(perc_file) as f:
            return float(f.readline())

    cv2.imwrite(source_file + '/tile.png', image)
    # image = cv2.imread(path)

    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        image = apply_brightness_contrast(image, 32, 0)

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        output = check_green(output)

        gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(gray_output, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        cv2.imwrite(analyzed_file + '/tile.png', im_bw)

        perc = treePer(im_bw)

        with open(perc_file, "w") as f:
            f.write(str(perc))

        return perc


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    resp = urllib.request.urlopen(req)

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def getRatio(z, lat, lng):
    return 156543.03392 * math.cos(float(lat) * math.pi / 180) / math.pow(2, int(z))


def getImageByXYZ(x, y, z, request, lat, lng):
    perc = analyze(x, y, z)

    analyzed_img = "{}/static/analyzed/{}/{}/{}/tile.png".format(request._current_scheme_host, z, x, y)
    source_img = "{}/static/source/{}/{}/{}/tile.png".format(request._current_scheme_host, z, x, y)

    area = getRatio(z, lat, lng) * perc / 100
    total_area = getRatio(z, lat, lng)

    return {'perc': perc, 'analyzed_img': analyzed_img, 'source_img': source_img, 'area': area,
            'total_area': total_area}
