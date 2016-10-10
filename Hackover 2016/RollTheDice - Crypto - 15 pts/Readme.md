# Hackover 2016 - Rollthedice
### Crypto - 15 pts

    The new cyber casinos are using high speed digital cyber dices to provide the best available gaming experience. Play a brand new dice game at new levels and win. Please note that you have to upgrade to blockchain 3.0 to receive your profits via a smart contract 2.0.
    
In this challenge, the server gives us his dice roll with a ciphertext base64 encoded.
We must send our own dice roll ciphertext in order to match the opposite face of thei dice roll. But we don't know yet the key they used and therefore their dice roll.
They then send their key, and finaly we send ours.

After a first attemps, by sending the same data as they send, the program tells us what was the roll dice they had and that our result isn't good. We decipher their dice roll (Using AES 128 ECB and it works !) and see that the plaintext is of the form :
`000X` followed by "random" bytes where X is the roll dice.

So we need to send a random cipher text, and then change our key in order to have a plaintext of the right form. An easy solution is to generate random key until it is OK. Iterating through all possible key until it works might be better, but the random solution solved the chall quickly and was easier to implement.

Then the code is pretty straigth forward :

```python
from Crypto.Cipher import AES
import os
import base64
import socket
import re

def solve(dice,key_dist):
	obj_dist = AES.new(base64.b64decode(key_dist), AES.MODE_ECB)
	plaintext = obj_dist.decrypt(base64.b64decode(dice)).encode('hex');
	wanted = 7 - int(plaintext[3]); # The sum of two opposite faces on a dice makes 7
	key = os.urandom(16)
	obj = AES.new(key, AES.MODE_ECB)
	message = "00000000000000000000000000000000".decode('hex')
	ciphertext = obj.decrypt(message)

	while(not str.startswith(ciphertext.encode('hex'),'000'+str(wanted))):
		key = os.urandom(16)
		obj = AES.new(key, AES.MODE_ECB)
		ciphertext = obj.decrypt(message)

	return base64.b64encode(key)

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('challenges.hackover.h4q.it', 1415))
	i = 0
	while True:
		data = s.recv(2048)
		if(i == 32):
			print "Received:", data
		if len(repr(data)) <=2 :
			break;
		mgex = re.search('My dice roll: ([a-zA-Z0-9+/]+==)', repr(data))
		if mgex != None:
			dice = mgex.group(1);
		mgex = re.search('Your dice roll',repr(data));
		if mgex != None:
			s.send("AAAAAAAAAAAAAAAAAAAAAA==\n")
		mgex = re.search('My key: ([a-zA-Z0-9+/]+==)', repr(data))
		if mgex != None:
			key = mgex.group(1);
		mgex = re.search('Your key:', repr(data))
		if mgex != None:
			s.send(solve(dice,key)+"\n");
			i+= 1;
			print "Solved ", i, "times"
		
	print "Connection closed."
	s.close()

main()
```