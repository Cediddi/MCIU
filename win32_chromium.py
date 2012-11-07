#! /bin/python3
# ------------------------------------------------------
# |   Mighty Chromium Installer and Updater rel 1.3    |
# ------------------------------------------------------
# | This Mighty Python Script downloads and  installs  |
# | or updates lastest Chromium build snapshot for Win |
# ------------------------------------------------------
# |           Copyright (c)  2012 Umut Karcı           |
# |            <umutkarci@std.sehir.edu.tr>            |
# ------------------------------------------------------
   
import shutil, urllib.request, zipfile, re, os, math, threading, time, sys
from threading import Thread

LAST=str(urllib.request.urlopen("https://commondatastorage.googleapis.com/chromium-browser-snapshots/Win/LAST_CHANGE").read())[2:-1]
ZIP=("https://commondatastorage.googleapis.com/chromium-browser-snapshots/Win/"+LAST+"/chrome-win32.zip")
ZIP_LOCAL=("C:\WINDOWS\Temp\chrome-win32.zip")
BIN_LOCAL=("C:\WINDOWS\Temp\chrome-win32")
APP_DIR=("C:\Program Files")
BIN_APP=(APP_DIR+"\chrome-win32")
VERSION_LOCAL=(BIN_APP+"\VERSION")

def f_downloader():
	print("Downloading")
	Thread(target = t_sizeprinter).start()
	if os.path.isfile(ZIP_LOCAL):
		os.remove(ZIP_LOCAL)
	open(ZIP_LOCAL,"w").close()
	urllib.request.urlretrieve (ZIP, ZIP_LOCAL)
	sys.stdout.write("\n")

def f_extracter():
	print("Extracting")
	zipfile.ZipFile(ZIP_LOCAL).extractall("C:\WINDOWS\Temp")

def f_installer():
	f = open("C:\WINDOWS\Temp\chrome-win32\VERSION", "w")
	f.write(LAST)
	f.close()
	os.system("TASKKILL /F /IM chrome.exe")
	time.sleep(3)
	if os.path.isdir(BIN_APP):
		shutil.rmtree(BIN_APP)
	print("Installing")
	shutil.move(BIN_LOCAL, APP_DIR)

def f_cleaner():
	print("Removing temp files")
	os.remove(ZIP_LOCAL)

def t_sizeprinter():
	SIZE = math.floor(int(urllib.request.urlopen(ZIP).info().get('Content-Length')))
	print("Total Size: ", math.floor(SIZE/1024**2), "MB")
	SIZE_LOCAL_PERCENT = "0.00"
	while SIZE_LOCAL_PERCENT != "100.":
		if os.path.isfile(ZIP_LOCAL):
			SIZE_LOCAL = math.floor(int(os.stat(ZIP_LOCAL).st_size))
			SIZE_LOCAL_PERCENT = str((SIZE_LOCAL*100)/SIZE)[:4]
			if math.floor(SIZE_LOCAL/1024**2) < 10:
				SIZE_LOCAL = "0"+str(math.floor(SIZE_LOCAL/1024**2))
			else:
				SIZE_LOCAL = str(math.floor(SIZE_LOCAL/1024**2))
			sys.stdout.write("Percent: %s %%  %s MB  \r" % (SIZE_LOCAL_PERCENT, SIZE_LOCAL))
		else:
			sys.stdout.write("Percent: %s %%  %s MB  \r" % ("0.00", "00"))

if os.path.isfile(VERSION_LOCAL):
	INFO_VERSION=open(VERSION_LOCAL, "r").read()
	VER=str(INFO_VERSION)
else:
	VER="0"
	print("App isn't installed yet.")
print("Last build: "+LAST)
print("Your build: "+VER)
if int(LAST) > int(VER):
	f_downloader()
	f_extracter()
	f_installer()
	f_cleaner()
else:
	print("Already Up To Date")