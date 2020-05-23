import os, glob
import requests
import time
from lxml import html

import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')

ndx = int(config['DEFAULT']['lastIndex'])
imgCount = int(config['DEFAULT']['imgCount'])

baseAddress = 'http://archillect.com/'
img_dir = "./img/"

if not os.path.exists(img_dir): os.makedirs(img_dir)

def searchIndex():
	step = imgCount;
	index = ndx;
	ub = 1E9*index;
	
	while(True):
		print("Searching last index... Current index: " + str(index) + " step " + str(step) + "... ", end='\n')
		if scrapeImg(index) == -1:
			ub = index
			step = int(step / 2)
			index -= step
			if step == 0 : return index
		else: 
			if index + 2*step < ub : step = 2*step
			if index + step >= ub: step = int(step/2)
			index += step

def scrapeImg(index):
	index = str(index)
	url = baseAddress + index
	r = requests.get(url)
	tree = html.fromstring(r.content)

	try:
		link = tree.xpath('//*[@id="ii"]/@src')[0] 								## [0]: retrieve the first element matching the criteria
		extIndex = link.rfind(".",0) 											## search backwards looking for the first "."
		fileExtention = link[extIndex:]											## retrieve the file basetype
		fileName = index + fileExtention
		return (fileName, link);

	except IndexError:
		print('Looks like '+ baseAddress + str(index) +' is not valid.')
		return -1;

def saveImg(fileName, fileAddress):
	print("Saving " + fileName)
	file = requests.get(fileAddress) 											## load the file to memory
		
	with open(img_dir + fileName, 'wb') as f: 
		f.write(file.content)
		f.close();

def eraseFiles():
	try:
		fileList = os.listdir("./img")
		while(len(fileList) > imgCount):
			
			os.remove("./img/" + fileList[0])
			fileList = os.listdir("./img")
	except: pass

ndx = searchIndex()																
print('Found index: ' + str(ndx))
ndx -= imgCount

while(1):
	f = scrapeImg(ndx)
	ndx += 1
	if f!=-1:
		print("Saving {}...".format(f[1]))
		saveImg(f[0], f[1])
	else:
		print("Erasing extra files...")
		eraseFiles();

		config['DEFAULT']['lastIndex'] = str(ndx)
		#config['DEFAULT']['imgCount'] = str(imgCount)
		config.write(open('./config.cfg','w'));
		
		print('Shutting down...')
		time.sleep(3);
		break;