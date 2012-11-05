#! /usr/local/bin/python3
# ------------------------------------------------------
# |   Mighty Chromium Installer and Updater rel 1.0    |
# ------------------------------------------------------
# | This Mighty Python Script downloads and  installs  |
# | or updates lastest Chromium build snapshot for OSX |
# ------------------------------------------------------
# |           Copyright (c)  2012 Umut Karcı           |
# |            <umutkarci@std.sehir.edu.tr>            |
# ------------------------------------------------------

import shutil, urllib.request, zipfile, re, os, math, time, sys
LAST=str(urllib.request.urlopen("https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/LAST_CHANGE").read())[2:-1]
ZIP=("https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/"+LAST+"/chrome-mac.zip")
ZIP_LOCAL=("/tmp/chrome-mac.zip")
BIN_LOCAL=("/tmp/chrome-mac/Chromium.app")
APP_DIR=("/Applications/")
BIN_APP=(APP_DIR+"Chromium.app")
PLIST_LOCAL=(BIN_APP+"/Contents/Info.plist")
if os.path.isfile(PLIST_LOCAL):
	INFO_PLIST=open(PLIST_LOCAL, "r").read()
	VER=str(re.findall("(?<=<string>)(\d{6})(?=</string>)", INFO_PLIST))[2:-2]
else:
	VER="0"
	print("App isn't installed yet.")
print("Last build: "+LAST)
print("Your build: "+VER)
if int(LAST) > int(VER):
	SIZE = math.floor(int(urllib.request.urlopen(ZIP).info().get('Content-Length'))/1024**2)
	print("Downloading")
	print("Total Size: ", SIZE, "MB")
	urllib.request.urlretrieve (ZIP, ZIP_LOCAL)
	sys.stdout.write("\n")
	print("Extracting")
	zipfile.ZipFile(ZIP_LOCAL).extractall("/tmp/")
	if os.path.isfile(PLIST_LOCAL):
		print("Installing")
		shutil.rmtree(BIN_APP)
		shutil.move(BIN_LOCAL, APP_DIR)
	else:
		print("Installing")
		shutil.move(BIN_LOCAL, APP_DIR)
	print("Setting permissions")
	for root, dirs, files in os.walk(BIN_APP):
		for filevar in dirs:
			os.chmod(os.path.join(root, filevar), 493)
		for filevar in files:
			os.chmod(os.path.join(root, filevar), 493)
	print("Removing temp files")
	shutil.rmtree("/tmp/chrome-mac/")
	os.remove(ZIP_LOCAL)
else:
	print("Already Up To Date")