import re

result = []
toAddList = []
toAdd = False

f = open('k.txt')
for line in f:
    if(toAdd):
        toAddList.append(line)
    if "Author: " in line:
        if(toAdd):
            result.append([line.split(':')[1], toAddList.copy()])
            toAddList.clear()
            toAdd = False
        if("fix:") in line:
            toAdd = True
        
print(result)