from Crypto.Cipher import AES
import os
import base64
import socket
import re

def solve(dice,key_dist):
	obj_dist = AES.new(base64.b64decode(key_dist), AES.MODE_ECB)
	plaintext = obj_dist.decrypt(base64.b64decode(dice)).encode('hex');
	# print plaintext[3];
	# print plaintext
	wanted = 7 - int(plaintext[3]);
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
			# print solve(dice,key);
			s.send(solve(dice,key)+"\n");
			i+= 1;
			print "Solved ", i, "times"
		
	print "Connection closed."
	s.close()


main()