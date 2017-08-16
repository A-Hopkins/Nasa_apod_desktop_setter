#!/usr/bin/env python

"""
Grabs the Nasa Astronomy Picture of the Day and downloads it then sets it as your wallpaper

HOW TO USE:
So far this script has only been tested on ubuntu. Here is how it was intended to be used:
1) Change the DOWNLOAD_PATH to where ever you want the picture to be downloaded from, default is home/Pictures/APOD/
   Note: Creates Pictures and APOD folder if not already there
2) Run on startup when you log on, be sure to stick in a scripts folder because it does create a log file if it fails.
"""
import logging
import os
from urllib import request
from urllib.error import URLError

from bs4 import BeautifulSoup

# Constants
DOWNLOAD_PATH = os.getenv("HOME") + '/Pictures/APOD/'
NASA_APOD_SITE = "http://apod.nasa.gov/apod/"

logging.basicConfig(filename='apod_log.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def download_image(site_url):
    """
    Downloads an image from the site url given

    Using request.urlopen to connect to the site, then the function uses BeautifulSoup to parse the html and look for
    the image tag which then saves it in the DOWNLOAD_PATH constant.

    :param site_url: a site url, ex: "http://apod.nasa.gov/apod/"

    :return: File - should return a file with
    """

    try:

        html = request.urlopen(site_url)
        soup = BeautifulSoup(html.read(), "lxml")
        logging.info("Connected to " + site_url)

        image = site_url + soup.find("img").parent.get("href")

        html_image = request.urlopen(image)

        image_file = open(DOWNLOAD_PATH + "apod.jpg", 'wb')
        image_file.write(html_image.read())
        image_file.close()

        return image_file

    except URLError as error:
        logging.critical(error)
        exit(1)

    except IOError as error:
        logging.critical(error)
        exit(1)


if __name__ == '__main__':

    if not os.path.exists(os.path.expanduser(DOWNLOAD_PATH)):
        os.makedirs(os.path.expanduser(DOWNLOAD_PATH))

    # Run script
    image_location = download_image(NASA_APOD_SITE)
    print(image_location.name)

    os.system("gsettings set org.gnome.desktop.background picture-uri " +
              "'file:///%s'" % image_location.name)
