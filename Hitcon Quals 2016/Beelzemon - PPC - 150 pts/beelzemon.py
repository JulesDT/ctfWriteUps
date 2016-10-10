'''
Pod for Team Fourchette Bombe
'''
import socket
import re
import operator
import time

def find_partition(int_list,n,k):
	len_A=0; len_B=0; sum_A=0; sum_B=0
	Aret = ""; Bret = ""

	for i in range(0,len(int_list)):
	    int_list[i] += 2**n
	int_list=int_list[::-1]
	for nb in int_list:
	    if nb == 0:
	        if len_A < len_B:
	            len_A+=1
	            Aret+= str(-2**n)+ " "
	        else:
	            len_B+=1
	            Bret+= str(-2**n)+ " "
	    else:
	        if sum_A < sum_B:
	           sum_A+=(nb**k)
	           len_A+=1
	           Aret+=str(nb-(2**n))+ " "
	        else:
	           sum_B+=(nb**k)
	           len_B+=1
	           Bret+=str(nb-(2**n))+ " "
	return (Aret)

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
			s.send(partition+'\n');
		
	print "Connection closed."
	s.close()
	print "Process duration :", time.time() - begin

main()