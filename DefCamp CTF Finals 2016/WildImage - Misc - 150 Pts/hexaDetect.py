from PIL import Image
import pytesseract
from os import listdir
from os.path import isfile, join

mypath = "./images"
onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.split('.')[-1] == 'png']
string = ""
for f in onlyfiles[1:]: #Avoiding openning the "DCTF" one
	im = Image.open(f)
	newIm = Image.new('RGB',im.size,"white")
	pixels = im.load()
	newPixels = newIm.load()
	for i in range (0,im.size[0]):
		for j in range(0,im.size[1]):
			if pixels[i,j] == (0,0,0):
				newPixels[i,j] = pixels[i,j]

	captchaRep = pytesseract.image_to_string(newIm,config="-psm 10")
	if captchaRep in "abcdef0123456789":
		newIm.save('hexa/'+f.split('/')[-1])