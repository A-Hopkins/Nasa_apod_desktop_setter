#!/usr/bin/env python

"""
Grabs the Nasa Astronomy Picture of the Day and downloads it then sets it as your wallpaper


"""
import os
from urllib import request

from bs4 import BeautifulSoup

DOWNLOAD_PATH = os.getenv("HOME") + '/Pictures/APOD/'
NASA_APOD_SITE = "http://apod.nasa.gov/apod/"


# TODO: add exception handling and logging for if site fails or download fails


def download_image(site_url):
    html = request.urlopen(site_url)
    soup = BeautifulSoup(html.read(), "lxml")

    image = site_url + soup.find("img").parent.get("href")

    html_image = request.urlopen(image)

    image_file = open(DOWNLOAD_PATH + "apod.jpg", 'wb')
    image_file.write(html_image.read())
    image_file.close()


if __name__ == '__main__':

    if not os.path.exists(os.path.expanduser(DOWNLOAD_PATH)):
        os.makedirs(os.path.expanduser(DOWNLOAD_PATH))

    # Run script
    download_image(NASA_APOD_SITE)
