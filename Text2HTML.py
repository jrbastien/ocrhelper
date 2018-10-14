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
	text = re.sub(r'([a-zA-Z0-9àâéùûœﬅﬁ:;,.\)])(<br>)([a-zA-Z0-9ſàâéèùûœ\&ﬁ\(])', r'\1 \3', text) # joining continuous text
	text = re.sub(r'(fig\.|Fig\.)(<br>)([0-9])', r'\1 \3', text) # joining continuous text
	
	text = re.sub(r'(anti-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(arcs-|arc-)(<br>)(boutant)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(arriere-|arrieres-)(<br>)(vou)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(au-|Au-)(<br>)(delà)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(au-|Au-)(<br>)(deus|deous)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(au-|Au-)(<br>)(devant)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(avant-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(à-)(<br>)(peu-près)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(bien-)(<br>)(tôt)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(celle-|celui-|ceux-)(<br>)([ci])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(ci-)(<br>)(après|devant)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(ci-|au-)(<br>)(de)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(contre-)(<br>)(haut|bas)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(cul-de-|cul-)(<br>)(nge|de-nge)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(cul-de-|cul-)(<br>)(lampe|de-lampe)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(contre-|haut|bas)(<br>)(de)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(demi-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(dis-)(<br>)(je)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(dix-|vingt-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(elle-|lui-)(<br>)(même)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(en-)(<br>)(bas|haut)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(entre-)(<br>)(elle)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(eux-|elles-)(<br>)(même)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(eﬅ-)(<br>)(à-dire)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(eﬅ-à-)(<br>)(dire)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(faites-)(<br>)(en)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(faux-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(long-)(<br>)(temps)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(mi-)(<br>)(parti)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(non-)(<br>)(ſeul)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(par-)(<br>)(tout|avant|derriere|de)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(peu-)(<br>)(près)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(peu-)(<br>)(à-peu)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(peu-à-)(<br>)(peu)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(peut-)(<br>)(être)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(plate-|plates-)(<br>)(bande)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(plein-)(<br>)(cintre)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(porte-|Porte-|Portes-)(<br>)(cochere)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(porte-)(<br>)(outil)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(que-)(<br>)(fois)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(rez-)(<br>)(de-chau)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(tout-)(<br>)(à-fait)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(tout-à-)(<br>)(fait)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(très-)(<br>)([a-zſàâéèùﬁﬂ\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(varlope-)(<br>)(onglet)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(vis-)(<br>)(à-vis)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(vis-à-)(<br>)(vis)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(verd-de-|verd-)(<br>)(gris|de-gris)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(à-)(<br>)(fait)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(ſur-)(<br>)([a-zſàâéèù\&])', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(ſerre-)(<br>)(papier)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(Chae-)(<br>)(pointe)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(Menuier-|Menuiers-)(<br>)(Ebéniﬅe)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(Porte-)(<br>)(aiguille)', r'\1\3', text) # joining hyphenated words
	text = re.sub(r'(Serrurier-|Serruriers-)(<br>)(Ferreur)', r'\1\3', text) # joining hyphenated words
	
	text = re.sub(r'([a-zàâéêùûôſﬅﬃﬁ])(\-<br>)([a-zſàâéèêùûôﬁﬂ])', r'\1\3', text) # removing false hyphenations

	# Converting to modern types
	text = re.sub(r'ſ', r's', text) # long S to regular S
	text = re.sub(r'ﬀ', r'ff', text) # ligature ﬀ to double fs
	text = re.sub(r'ﬁ', r'fi', text) # ligature ﬁ to separate fi
	text = re.sub(r'ﬂ', r'fl', text) # ligature ﬂ to separate fl
	text = re.sub(r'ﬃ', r'ffi', text) # ligature ﬃ to separate ffi
	text = re.sub(r'ﬄ', r'ffl', text) # ligature ﬄ to separate ffi
	text = re.sub(r'ﬅ', r'st', text) # ligature ﬅ to regular st
	text = re.sub(r'', r'si', text) # ligature long s-i to separate si
	text = re.sub(r'', r'ss', text) # ligature double long s to separate ss
	text = re.sub(r'', r'ssi', text) # ligature double long s-i to separate ssi
	text = re.sub(r'', r'ct', text) # ligature ct to separate ct


	with open(inputfile[:-4]+".html", 'w') as file: 
		file.write(text) # rewrite the file
