#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image
import cv2
import numpy as np
import pytesseract
import os
import codecs
import re
import shutil

MAX_HEIGHT = 83		# Max % of page height that can be a text block - anything larger is discarded
MAX_WIDTH = 78		# Max % of page width that can be a text block - anything larger is discarded
MIN_HEIGHT = 1.4	# Min % of page height that can contain text - anything smaller is discarded
MIN_WIDTH = 7.8		# Min % of page width that can contain text - anything smaller is discarded.

DILATATION_ITERATIONS = 15 # Number of dilatations needed around text to create valid contours

TEXT_EXCLUSION = 'MENU'
TEXT_LANGUAGE = 'rbo'


# Create a special function to sort files by number (300 prior to 1600 for instance)
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# create subdirectory for cropped images
subfolder = "cropped"
shutil.rmtree(subfolder, ignore_errors=True)
if not os.path.exists(subfolder):
	for retry in range(100):
		try:
			os.makedirs(subfolder)
			break
		except:
			print "Cropped folder creation failed, retrying..."

# get current folder info
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)

# Find regions of interest and save them to separate file
filecount = 0
for file in os.listdir(dirpath):
     if os.path.isfile(os.path.join(dirpath, file)):
	if os.path.splitext(file)[1].lower() in ('.png'):
			filecount = filecount + 1	
			image = Image.open(file)
			width, height = image.size
			print("Cropping images for " + str(file))
			image = cv2.imread(file)
			gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale

			
			# template matching and replacement
			prevpt = 0
			template = cv2.imread('opencv-template-for-matching.jpg',0)
			w, h = template.shape[::-1]
			res = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
			threshold = 0.6
			loc = np.where( res >= threshold)
			for pt in zip(*loc[::-1]):
				#cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
				cv2.rectangle(gray, pt, (pt[0] + w, pt[1] + h +50), 230, -1) #fill the matched area with grey on grayscale image.
				if pt[1] > prevpt + 20:
					print('Template match found at ' + str(pt))
					crop_img = image[pt[1]+45:pt[1] + h +45, pt[0]:pt[0] + w]
					crop_img_w_border = cv2.copyMakeBorder(crop_img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
					 #white border helps the OCR
					filename = os.path.splitext(file)[0] + "_cropped_%d.png" % pt[1]
					cv2.imwrite(os.path.join(subfolder, filename), crop_img_w_border)
					cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h +50), [255,255,255], -1) #fill the matched area with white on original image.
					prevpt = pt[1]
			
			# retrieve contours for remaining blocks
			_,thresh = cv2.threshold(gray,125,255,cv2.THRESH_BINARY_INV) # threshold
			#cv2.waitKey(0)
			kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,3))
			dilated = cv2.dilate(thresh,kernel,iterations = max(DILATATION_ITERATIONS*width/1900, DILATATION_ITERATIONS)) # dilate x times or more if page is larger
			#cv2.imshow('Dilated',dilated)
			#cv2.waitKey(0)
			_, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

			# for each contour found, draw a rectangle around it on original image
			contourcount = 0			
			for contour in contours:
				# get rectangle bounding contour
				[x,y,w,h] = cv2.boundingRect(contour)
			 

				# discard areas that are too large
				if h>(float(MAX_HEIGHT)/100*height) and w>(float(MAX_WIDTH)/100*width):
					continue

				# discard areas that are too small
				if h<(float(MIN_HEIGHT)/100*height) or w<(float(MIN_WIDTH)/100*width):
					continue

				contourcount= contourcount + 1	
				crop_img = image[y:y+h, x:x+w]
				#cv2.imshow("cropped%d.png" %i, crop_img)
				crop_img_w_border = cv2.copyMakeBorder(crop_img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255]) #white border helps the OCR
				
				filename = os.path.splitext(file)[0] + "_cropped_%d.png" % y
				cv2.imwrite(os.path.join(subfolder, filename), crop_img_w_border)
				#cv2.waitKey(0)
				
				# draw rectangle around contour on original image
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
			 
			# write original image with added contours to disk 			
			cv2.imwrite(os.path.splitext(file)[0] + "_contoured.jpg", image) 
			# cv2.destroyAllWindows()
			if contourcount == 0:
				print ('No block of text found, writing the entire image')
				cv2.imwrite(os.path.join(subfolder, file), image)
if filecount == 0:
	print ('There is no png to process')
	exit()

# Perform OCR on cropped files
ocrfile = foldername + ".txt"
f = open(ocrfile,"w")
for root, dirs, filenames in os.walk(subfolder):
    for file in sorted(filenames, key=numericalSort):
		print("Performing OCR on " + str(file))
		text = pytesseract.image_to_string(Image.open(os.path.join(subfolder, file)), lang=TEXT_LANGUAGE, config="-c tessedit_char_blacklist=%").encode('utf-8')
		if text[:4] == TEXT_EXCLUSION:
			print('Excluding block of text starting with ' + TEXT_EXCLUSION)
		else:
			f.write(text + '\n\r')
f.close()

# Fixing common OCR errors
# Performing Search and replace with dictionary OCRFix.txt
print('Fixing common OCR errors')

rep = {} # creation of empy dictionary

with open('OCRFix.txt') as temprep: # loading of definitions in the dictionary
    for line in temprep:
        (key, val) = line.strip('\n').split('|')
        rep[key] = val

with open (ocrfile, "r") as textfile: # load each file in the variable text
	text = textfile.read()

	# start replacement
	#rep = dict((re.escape(k), v) for k, v in rep.items()) commented to enable the use in the mapping of re reserved characters
	pattern = re.compile("|".join(rep.keys()))
	#print (pattern)
	text = pattern.sub(lambda m: rep[m.group(0)], text)

	#write of te output files with new suffice
	target = open(ocrfile[:-4]+"_OCRFix.txt", "w")
	target.write(text)
	target.close()

# Removing empty lines
with open(ocrfile[:-4]+"_OCRFix.txt") as file: 
    text = file.read() # read file into memory
text = re.sub(r'([a-zàé,:])(\n\n)([a-zſ&])', r'\1\n\3', text) # remove empty line between words
text = re.sub(r'([a-zàé]\-)(\n\n)([a-zſ])', r'\1\n\3', text) # remove empty line between hyphenation
text = re.sub(r'([a-zàé]\—)(\n\n)([a-zſ])', r'\1\n\3', text) # remove empty line between hyphenation

# Fixing invalid spacing with comma and semicolon 
text = re.sub(r'([a-zA-Z0-9\)àâéèù])(,)([a-zA-Zſàâéèù&0-9])', r'\1, \3', text)
text = re.sub(r'([a-zA-Z0-9\)àâéèù])( , )([a-zA-Zſàâéèù&0-9])', r'\1, \3', text)
text = re.sub(r'([a-zA-Z0-9\)àâéèù])( ,)(\n)', r'\1,\3', text)
text = re.sub(r'(\s)(,)([a-zA-Zſàâéèù&0-9])', r', \3', text)
text = re.sub(r'(\s)(;)([a-zA-Zſàâéèù&\s])', r'\2\3', text)

# Fixing spaces before and after parenthesis
text = re.sub(r'(\()(\s)([a-zA-Zſ\*])', r'\1\3', text)
text = re.sub(r'([a-zA-Z0-9\.\*])(\s)(\))', r'\1\3', text)

# Fixing spaces before and after hyphens
text = re.sub(r'([a-zàâéù])(- )([a-zſàâéèù])', r'\1-\3', text)
text = re.sub(r'([a-zàâéù])( -)([a-zſàâéèù])', r'\1-\3', text)
text = re.sub(r'([a-zàâéù])( - )([a-zzſàâéèù])', r'\1-\3', text)

# Fixing spaces before and after ampersands
text = re.sub(r'([a-z0-9àâéù])(& )([a-zA-Z0-9ſàâéèù])', r'\1 & \3', text)
text = re.sub(r'([a-z0-9àâéù])( &)([a-zA-Z0-9ſàâéèù])', r'\1 & \3', text)

# Fixing spaces after periods
text = re.sub(r'(\.)([A-Z0-9])', r'\1 \2', text)

# Cleaning extra characters at end of paragraphs
text = re.sub(r'\._', r'.', text)
text = re.sub(r'\. \.‘',r'.', text)

# Cleaning extra characters at begining of paragraphs
text = re.sub(r'\n(\.|-)(\s)([a-zA-Z])', r'\n\3', text)

#Fixing Os read as zeros
text = re.sub(r'([a-zA-Zé’])(0)', r'\1o', text)
text = re.sub(r'(0)([a-zA-Zé’])', r'o\1', text)

with open(ocrfile[:-4]+"_OCRFix.txt", 'w') as file: 
	print('Writing final OCR to ' + str(ocrfile[:-4]+"_OCRFix.txt") )
	file.write(text) # rewrite the file
