#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re


if len(sys.argv) < 2:
	print 'usage:', sys.argv[0], 'TEXTFILE1 [TEXTFILE2 ...]'
	sys.exit(0)

for inputfile in sys.argv[1:]:

	
	with open(inputfile, 'rU') as file: 
		text = file.read() # read file into memory
	text = re.sub(r'[ \t]+\n', r'\n', text) # remove trailing spaces
	text = re.sub('&', '&amp;', text) # convert ampersand symbols to html entities
	text = re.sub('<', '&lt;', text) # convert less than symbols to html entities
	text = re.sub('>', '&gt;', text) # convert greater than symbols to html entities
	text = re.sub(r'((?m)^[ \t]*$\n?)', r'\n', text) # Removing empty lines

	# html creation
	text = re.sub(r'\n', '<br>', text)
	text = re.sub('<br>\s*<br>', '</p>\n\t<p>', text)
	text = re.sub('<p><br/>', '', text)
	text = re.sub(r'\A', r'<head>\n\t<meta charset="utf-8"/>\n</head>\n<body>\n\t<p>', text)
	text = re.sub(r'$', r'</p>\n</body>', text)
	
	# Rebuilding Paragraphs
	text = re.sub(r'([a-zàâéù,;])(<br>)([a-zſàâéèù&])', r'\1 \3', text)
	# text = re.sub(r'([a-zàâéù])(-<br>)([a-zſàâéèù])', r'\1\3', text) #optional: can truncate real hyphenations
		
	with open(inputfile[:-4]+".html", 'w') as file: 
		file.write(text) # rewrite the file
