'''
Pod for Team Fourchette Bombe
'''
import socket
import re
import operator
import time

def find_partition(int_list,n,k):
	A = []
	B = []
	Aret = []
	Bret = []
	for i in range(0,len(int_list)):
		int_list[i] += 2**n
	
	for nb in sorted(int_list, reverse=True):
		if nb == 0:
			if len(A) < len(B):
				A.append(0)
				Aret.append(-2**n)
			else:
				B.append(0)
				Bret.append(-2**n)
		else:
			if sum(A) < sum(B):
			   A.append(nb**k)
			   Aret.append(nb-2**n)
			else:
			   B.append(nb**k)
			   Bret.append(nb-2**n)
	return (Aret, Bret)

def main():
	begin = time.time()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('52.198.217.117', 6666))
	while True:
		data = s.recv(2048)
		print "Received:", data
		if len(repr(data)) <=2 :
			break;
		mgex = re.search('([0-9]+) ([0-9]+)', repr(data))
		if mgex != None:
			n = long(mgex.group(1));
			k = long(mgex.group(2));
			mySet = range(-2**n,2**n);
			partition = find_partition(mySet,n,k)
			final = ''
			for p in partition[1]:
				final += ' '+str(p)
			s.send(final[1:]+'\n');
		
	print "Connection closed."
	s.close()
	print "Process duration :", time.time() - begin

main()