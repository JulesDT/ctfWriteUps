from PIL import Image

im = Image.open( 'planet.png' )
newIm = Image.new('RGB',(100,66),"yellow");

pixels = newIm.load()
pixelsIm = im.load()

for i in range(0,100):
	for j in range(0,66):
		pixels[i,j] = pixelsIm[i*24,j*24]

newIm.show()
newIm.save('final.png');