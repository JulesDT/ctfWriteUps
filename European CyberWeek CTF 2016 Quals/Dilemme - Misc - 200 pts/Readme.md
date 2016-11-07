# European CyberWeek 2016 Quals - Dilemme
### Misc - 200 pts

The challenge gives us a captcha and a QRCode to read in a limited time. Reading the QRCode is pretty straightforward with `qrtools`
For the captcha, there's custom lines printed on the image. But the message is in red and the lines in a kind of blue (Colorblind here ! \o/)
We just need to check the RGB code of each pixel and transform it to white if it's the color of the lines. Then tesseract will work perfectly without the lines !

The code is pretty straightforward and allows us to get a new QrCode and a new captcha giving the wanted flag

```python
from PIL import Image
import requests
from bs4 import BeautifulSoup
import base64
from io import BytesIO
import pytesseract
import qrtools

cookies=dict(session='XXXXXXX')
r = requests.get('https://challenge-ecw.fr/chals/divers200',cookies=cookies)
cook = r.cookies
dom = BeautifulSoup(r.text,'html.parser')
data = dom.findAll("img", {"alt" : "Captcha"})[0]['src']

im = Image.open(BytesIO(base64.b64decode(data[21:])))
im = im.convert('RGB');
im.save('check.png');
newIm = Image.new('RGB',im.size,"white");
pixels = im.load()
newPixels = newIm.load()

for i in range (0,im.size[0]):
	for j in range(0,im.size[1]):
		if pixels[i,j] != (20,40,100) and pixels[i,j] != (255,255,255):
			newPixels[i,j] = pixels[i,j];

captchaRep = pytesseract.image_to_string(newIm)

data = dom.findAll("img", {"alt" : "QRCode"})[0]['src']

im = Image.open(BytesIO(base64.b64decode(data[21:])))
im = im.convert('RGB');
im.save('qrcode.png')
qr = qrtools.QR()
qr.decode('qrcode.png')
qrRep = qr.data

print captchaRep,qrRep

req = dict(captcha=captchaRep,qrcode=qrRep,nonce="XXXXX")
r = requests.post('https://challenge-ecw.fr/chals/divers200',cookies=cook,data=req)
print r.text

fh = open('new.html','wb')
fh.write(r.text.encode('utf-8'))
fh.close()

dom = BeautifulSoup(r.text,'html.parser')
data = dom.findAll("img", {"alt" : "Captcha Win"})[0]['src']


im = Image.open(BytesIO(base64.b64decode(data[21:])))
im = im.convert('RGB');
im.save('checkWin.png');
data = dom.findAll("img", {"alt" : "QRCode Win"})[0]['src']

im = Image.open(BytesIO(base64.b64decode(data[21:])))
im = im.convert('RGB');
im.save('qrcodeWin.png')
```