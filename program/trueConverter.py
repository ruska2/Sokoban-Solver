import sys
l = []

with open("result", 'r') as file:
        for line in file:
            l = line.split(" ")


        with open("outsat",'r') as file:
            k = []
            start = False
            for line in file:
                if "Variables" in line:
                    start = True
                    continue
                if start:
                    k.append(line.split())
        s = []
        for i in l:
                if int(i) > 0:
                    for j in k:
                        iss = len(i)
                        if i in j[:6+iss]:
                            s.append(j[2])

	with open("finalresult", 'w') as out:    
            for i in s:
                if "move(p" in i:
                   out.write(i+"\n")

            for i in s:
                if "move(b" in i:
                    out.write(i+"\n")

            for i in s:
                if "at(b" in i:
                    out.write(i+"\n")
            for i in s:
                if "at(p" in i:
                    out.write(i+"\n")


