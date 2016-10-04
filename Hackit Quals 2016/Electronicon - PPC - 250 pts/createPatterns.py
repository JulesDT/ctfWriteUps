'''
Pod for Team Fourchette Bombe
'''
import codecs
f = codecs.open('pain.txt',encoding='utf-8')
flines = f.readlines()

length = 13
multiplier = 1
offset = multiplier*length

line = ''
for i in range(0,len(flines)):
	for j in range(0,length):
		line += flines[i][j+offset];
	line += '\n'
out = codecs.open('painPatterns/out','w', encoding='utf-8')
out.write(line)