#! python3

type = { "57" : "ID", 
		 "53" : "x coord", 
		 "54" : "y coord", 
		 "48" : "width major", 
		 "49" : "width minor", 
		 "58" : "pressure", 
		  "2" : "touch end", 
		  "0" : "end" }
		
interested_numbers = [0, 3]



lines = open('geteventFile.txt').read().split('\n')
output = ""

for i in range(len(lines)):
	e = lines[i].split(' ')
	output += e[0] + " "
	output += e[1] + " "
	output += '{0:0>4}'.format(str(int(e[2], 16))) + " "
	output += '{0:0>4}'.format(str(int(e[3], 16))) + " "
	if int(e[1], 16) in interested_numbers:
		output += type[str(int(e[2], 16))]
	output += "\n"

o = open('geteventFile_parsed.txt', 'w')
o.write(output)
