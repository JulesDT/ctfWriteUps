# Hackit 2016 Quals - Handmade encryption standard
### Crypto - 250 pts

    EN: Implementing of the latest encryption system as always brought a set of problems for one of the known FSI services: they have lost the module which is responsible for decoding information. And some information has https://ctf.com.ua/data/attachments/planet_982680d78ab9718f5a335ec05ebc4ea2.png.zipeen already ciphered! Your task for today: to define a cryptoalgorithm and decode the message.
    h4ck1t{str(flag).upper()}

In this challenge, we're given a picture which is a beautiful wallpaper

![Space Wallpaper](planet.png)

If we look carefully at this picture, and we zoom a bit, we can see little pixels that are differents

![Zoom on the wallpaper](planet_zoom.png)

Theses pixels are placed every 25 pixels (24 "normal" pixels between each "abnormal" pixel)

So we try to create an image with only theses pixels. We got this tiny python code :

```python
'''
Pod for Team Fourchette Bombe
'''
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
```

And the image we receive gives us the flag :

![recovered image](final.png)

Flag : h4ck1t{SPACE_IS_THE_KEY}