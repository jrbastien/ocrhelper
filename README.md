# ocrhelper
Tools to improve the OCR accuracy of old books

## Prerequisites

- python 2.7
- Pillow
- OpenCV
- numpy
- pytesseract

## Installation
Execute following commands to install the required libraries:
```sh
$ pip install pillow
$ pip install opencv
$ pip install numpy
$ pip install pytesseract
```

## Workflow
1. Create a directory with the individual PNG images of the chapter you want to OCR
2. Copy  BlockTextExtract.py, OCRFix.txt and Text2HTML.py to the same directory
3. Execute the first script:
    ~$ python BlockTextExtract.py
4. The resulting OCR is now [FolderName]_OCRFix.txt.  Each block of text is shown on a new file named image_contoured.jpg
5. Look at the results and adjust OCRFix.txt and/or script (see the Tweaks section below) as required then re-run the BlockExtract.py script.  If there is enough corrections and that the content of your book is pretty much standard across all chapters, this should be enough to process all the other chapters.
6. Convert to HTML if needed.  Before doing this, it is preferable to fix all invalid spaces between paragraphs.  Then execute:
    ~$ python Text2HTML.py [FolderName]_OCRFix.txt

## Tweaks

- In BlockTextExtract.py, you may want to change the size of the areas to discard based on the size of your scan.  For the small areas, you might want to discard any page numbers, for the large area, you are trying to exclude a large contour that would include the entire page.
- The language of the OCR training file needs to be changed to your language.  It is currently lang="frm" to recognize medieval French.
- Certain characters can be excluded from the OCR.  Currently, it only excludes %.  Modify tessedit_char_blacklist= as needed.
- Specify the text in the header or in the footer of the page that you want to exclude.  Currently it is "if text[:4] == 'MENU':".  This is to exclude any footer with "MENUISIER" in it.
- OCRFix.txt is a dictionary of words to be corrected.  The left end side of the pipe delimiter is the word to correct, the right end side, the corrected word.  Adjust as necessary based on your results.

- In Text2HTML.py, you might want to uncomment "text = re.sub(r'([a-zàâéù])(-<br>)([a-zſàâéèù])', r'\1\3', text)".  This will remove line breaks after hyphens and rebuild the 2 parts of the word together.  This is ok if your text does not contain a lot of words with natural hyphenation.  For instance, this might lead to convert "Full-time" to "fulltime".


## To conclude
If you find these helpers helpful, let me know and if you have any suggestions to improve them, I would be glad to know what they are.

<img src="https://raw.githubusercontent.com/ocrhelper/master/samples/gri_33125009321551_0187_contoured.jpg" alt="image" width=auto>


