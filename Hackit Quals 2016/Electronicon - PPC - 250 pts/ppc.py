'''
Pod for Team Fourchette Bombe
'''
import codecs
f = codecs.open('pain.txt',encoding='utf-8')
flines = f.readlines()

chars = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')

solve = ''

for i in range(0,len(flines[0]),13):
	for j in range(0,len(chars)):
		fp = codecs.open('./painPatterns/'+chars[j], encoding='utf-8')
		lines = fp.readlines() 
		Found = True
		for l in range(0,11):
			newI = i
			for c in range(0,13):
				if ((flines[l][i+c] == ' ' and lines[l][c] != ' ') or (flines[l][i+c] != ' ' and lines[l][c] == ' ')):
					Found = False;
					break;

			if not Found:
				break;
		if Found:
			solve += chars[j];
			break;

endf = open('solve','w');
endf.write(solve.decode('hex'));