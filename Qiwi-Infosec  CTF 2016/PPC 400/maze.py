#################################
# Pod for Team Fourchette Bombe #
#################################

import sqlite3
from PIL import Image
from mazeastar import astar
import numpy

conn = sqlite3.connect("maze.db")
c = conn.cursor()
w, h = 50,50
size = 10
MatrixGate = [[0 for x in range(w)] for y in range(h)]
MatrixValue = [[0 for x in range(w)] for y in range(h)]
for row in c.execute('SELECT * FROM points'):
	if row[3] == 'gate':
		MatrixGate[row[1]][row[2]] = 0
	else:
		MatrixGate[row[1]][row[2]] = 1
	MatrixValue[row[1]][row[2]] = row[4]

im = Image.new('RGB',(w*size,h*size),"black")
pixels = im.load()
for x in range(0,w):
	string = ""
	for y in range(0,h):
		if MatrixGate[x][y] == 0:
			for i in range(0,size):
				for j in range (0,size):
					pixels[size*x+i,size*y+j] = (255,255,255)

customArray = []
for i in range(0,50):
	customArray.append(MatrixGate[i])

nmap = numpy.array(customArray)
    
sol = astar(nmap, (0,0), (49,49))+[(0, 0)]

string = ""
for x in sol[::-1]:
	for i in range(0,size):
		for j in range (0,size):
			pixels[x[0]*size+i,x[1]*size+j] = (100,100,255)
	string += MatrixValue[x[0]][x[1]]

for i in range(0,size):
	for j in range (0,size):
		pixels[0+i,0+j] = (255,0,0)
		pixels[size*49+i,size*49+j] = (0,255,0)

im.show()
print string