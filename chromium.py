#! /usr/local/bin/python3
# ------------------------------------------------------
# |   Mighty Chromium Installer and Updater rel 1.3    |
# ------------------------------------------------------
# | This Mighty Python Script downloads and  installs  |
# | or updates lastest Chromium build snapshot for OSX |
# ------------------------------------------------------
# |           Copyright (c)  2012 Umut Karci           |
# |            <umutkarci@std.sehir.edu.tr>            |
# ------------------------------------------------------

import shutil
from urllib import request
import zipfile
import re
import os
import math
import sys
from threading import Thread


LAST = str(request.urlopen(
    "https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/LAST_CHANGE").read())[2:-1]
ZIP = ("https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/" + LAST + "/chrome-mac.zip")
ZIP_LOCAL = ("/tmp/chrome-mac.zip")
BIN_LOCAL = ("/tmp/chrome-mac/Chromium.app")
APP_DIR = ("/Applications/")
BIN_APP = (APP_DIR + "Chromium.app")
PLIST_LOCAL = (BIN_APP + "/Contents/Info.plist")


def f_downloader():
    print("Downloading")
    Thread(target=t_sizeprinter).start()
    request.urlretrieve(ZIP, ZIP_LOCAL)
    sys.stdout.write("\n")


def f_extracter():
    print("Extracting")
    zipfile.ZipFile(ZIP_LOCAL).extractall("/tmp/")


def f_installer():
    if os.path.isfile(PLIST_LOCAL):
        print("Installing")
        shutil.rmtree(BIN_APP)
        shutil.move(BIN_LOCAL, APP_DIR)
    else:
        print("Installing")
        shutil.move(BIN_LOCAL, APP_DIR)


def f_permissioner():
    print("Setting permissions")
    for root, dirs, files in os.walk(BIN_APP):
        for filevar in dirs:
            os.chmod(os.path.join(root, filevar), 493)
        for filevar in files:
            os.chmod(os.path.join(root, filevar), 493)


def f_cleaner():
    print("Removing temp files")
    shutil.rmtree("/tmp/chrome-mac/")
    os.remove(ZIP_LOCAL)


def t_sizeprinter():
    SIZE = math.floor(int(request.urlopen(ZIP).info().get('Content-Length')))
    print("Total Size: ", math.floor(SIZE / 1024 ** 2), "MB")
    if os.path.isfile(ZIP_LOCAL):
        os.remove(ZIP_LOCAL)
    SIZE_LOCAL_PERCENT = "0.00"
    while SIZE_LOCAL_PERCENT != "100.":
        if os.path.isfile(ZIP_LOCAL):
            SIZE_LOCAL = math.floor(int(os.stat(ZIP_LOCAL).st_size))
            SIZE_LOCAL_PERCENT = str((SIZE_LOCAL * 100) / SIZE)[:4]
            if math.floor(SIZE_LOCAL / 1024 ** 2) < 10:
                SIZE_LOCAL = "0" + str(math.floor(SIZE_LOCAL / 1024 ** 2))
            else:
                SIZE_LOCAL = str(math.floor(SIZE_LOCAL / 1024 ** 2))
            sys.stdout.write("Percent: %s %%  %s MB  \r" % (SIZE_LOCAL_PERCENT, SIZE_LOCAL))
        else:
            sys.stdout.write("Percent: %s %%  %s MB  \r" % ("0.00", "00"))


if os.path.isfile(PLIST_LOCAL):
    INFO_PLIST = open(PLIST_LOCAL, "r").read()
    VER = str(re.findall("(?<=<string>)(\d{6})(?=</string>)", INFO_PLIST))[2:-2]
else:
    VER = "0"
    print("App isn't installed yet.")
print("Last build: " + LAST)
print("Your build: " + VER)
if int(LAST) > int(VER):
    f_downloader()
    f_extracter()
    f_installer()
    f_permissioner()
    f_cleaner()
else:
    print("Already Up To Date")