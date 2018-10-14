#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import numpy as np
try:
    import Image as im
except ImportError:
    from PIL import Image as im
from scipy.ndimage import interpolation as inter
import os

# get current folder info
dirpath = os.getcwd()
print("\nProcessing all folders in : " + dirpath)


# process cropfolders as individual chapters
exclude = set(['cropped','exclusion','contoured','0-Exclusion', 'deskewed'])

for root, subdirs, files in os.walk(dirpath, topdown=True):
	subdirs[:] = [d for d in subdirs if d not in exclude] 
	for dirname in sorted(subdirs):
		filepath = os.path.join(root, dirname)
		foldername = dirname
		print("\nProcessing files in folder : " + foldername)

		# Find regions of interest and save them to separate file
		for file in os.listdir(filepath):
			if os.path.isfile(os.path.join(filepath, file)):
				if os.path.splitext(file)[1].lower() in ('.png'):
					img = im.open(os.path.join(filepath, file))
					# convert to binary
					wd, ht = img.size
					pix = np.array(img.convert('1').getdata(), np.uint8)
					bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)
					#plt.imshow(bin_img, cmap='gray')
					#plt.savefig('binary.png')


					def find_score(arr, angle):
					    data = inter.rotate(arr, angle, reshape=False, order=0)
					    hist = np.sum(data, axis=1)
					    score = np.sum((hist[1:] - hist[:-1]) ** 2)
					    return hist, score


					delta = 0.25
					limit = 3
					angles = np.arange(-limit, limit+delta, delta)
					scores = []
					for angle in angles:
					    hist, score = find_score(bin_img, angle)
					    scores.append(score)

					best_score = max(scores)
					best_angle = angles[scores.index(best_score)]
					print('Best angle: {}'.format(best_angle))

					# correct skew
					#data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
					#img = im.fromarray((255 * data).astype("uint8")).convert("RGB")
					deskewedfolder = 'deskewed'
					deskewedpath = os.path.join (deskewedfolder, dirname) 
					if not os.path.exists(deskewedpath):
						os.makedirs(deskewedpath)
					img.rotate(best_angle).save(os.path.join(deskewedpath, file))
					#img.save('skew_corrected.png')

