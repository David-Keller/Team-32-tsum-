#! python3
# https://github.com/fireflyes/Team-32-tsum-
type = { "57" : "ID", 
		 "53" : "x coord", 
		 "54" : "y coord", 
		 "48" : "width major", 
		 "49" : "width minor", 
		 "58" : "pressure", 
		  "2" : "touch end", 
		  "0" : "end" }
		
interested_numbers = [0, 3]

eventDevice = "/dev/input/event0"
adb = "adb shell "

def run(command):
    print("running {}{}".format(adb, command))
    return os.popen(adb + command).read()

def fromFile():
    lines = open('event').read().split('\n')
    output = ""
    
    for i in range(len(lines)):
            e = lines[i].split(' ')

        #if int(e[0], 16) in interested_numbers:
            line = "sendevent " + eventDevice + " "
            line += e[0] + " "
            line += '{0:0>4}'.format(str(int(e[1], 16))) + " "
            line += '{0:0>4}'.format(str(int(e[2], 16))) + ""

            #line += " # " + type[str(int(e[2], 16))]
        #    output += type[str(int(e[2], 16))]
            output += line
            output += "\n"

    o = open('event_parsed', 'w')
    o.write(output)

fromFile()
