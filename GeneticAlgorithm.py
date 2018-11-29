
'''
    Elliot Jordan
    AI Search
'''

import random
import copy

#load file and convert to list
file = open("AISearchfile012.txt","r")
fileString = file.read()
fileString = fileString.replace("\n", "").replace("\r","")
fileList = []
file.close()

# One string (one line) created
for char in fileString:
    if char.isalpha() or char == "=" or char == " ":
        fileString = fileString.replace(char,'')

# dirt and non-numbers (and commas) removed
fileList = fileString.split(",")
# List created
del fileList[0]
length = int(fileList[0])
del fileList[0]

# Use length to create matrix, populate with list
M = [[-1 for i in range(length+1)]for j in range(length+1)]
# Matrix M has all elements -1 (considered empty)

loc = 0
# Embedded for loops populate matrix M
for i in range(1,length):
    for j in range(1,length-i+1):
        M[i][j+i] = int(fileList[loc])
        loc+=1
# Second pair of for loops add 0's for (a,a) pairs, and -1 for the 0th city (for referencing so starts at 1)
for i in range(0,length+1):
    for j in range(0,length+1):
        if i == j:
            M[i][j] = 0
        if M[i][j] == -1:
            M[i][j] = M[j][i]
# Matrix is filled with values so M[i][j] = distance from i to j (empty row and column exists for non-existent city 0)

# creates a gene pool of random solutions to TSP
nodes = range(1,length+1)
genePool = []
for i in range(25*length):
    path = random.sample(nodes, len(nodes))

    # Calculate tour costs

    cost = 0
    for j in range(0, len(path)):
        x = path[j]
        if j < len(path) - 1:
            y = path[j + 1]
            # Add transition between j, j+1 nodes in ith tour
        else:
            y = path[0]
            # Adds transition to start node
        cost += M[x][y]
    genePool.append([cost, path])
genePool = sorted(genePool)


bestRoute = genePool[0]
for i in range(10):
    print(str(2*i) + "%")
    genePoolNew = []
    while len(genePoolNew) < len(genePool):
        #Creates random a
        a = random.random()
        d = []
        # If statements fill d with potential parents according to a probability (better = more likely)
        if a<0.5:
            for i in range(int(len(genePool)/4)):
                d.append(genePool[i])
        elif a<0.75:
            for i in range(int(len(genePool)/4),int(len(genePool)/2)):
                d.append(genePool[i])
        elif a<0.9:
            for i in range(int(len(genePool)/2),int(3*len(genePool)/4)):
                d.append(genePool[i])
        else:
            for i in range(int(3*len(genePool)/4),int(len(genePool))):
                d.append(genePool[i])
        parent1 = random.choice(d)

        # Creates random b
        a = random.random()
        d = []
        # If statements fill d with potential parents according to a probability (better = more likely)
        if a < 0.5:
            for i in range(int(len(genePool) / 4)):
                d.append(genePool[i])
        elif a < 0.75:
            for i in range(int(len(genePool) / 4), int(len(genePool) / 2)):
                d.append(genePool[i])
        elif a < 0.9:
            for i in range(int(len(genePool) / 2), int(3 * len(genePool) / 4)):
                d.append(genePool[i])
        else:
            for i in range(int(3 * len(genePool) / 4), int(len(genePool))):
                d.append(genePool[i])
        parent2 = random.choice(d)
        child = []
        childCost = 0
        legitimates = []
        for p in range(1, length+1):
            legitimates.append(p)
        start = random.choice(legitimates)
        child.append(start)
        legitimates.remove(start)
        q=start
        while len(child)<length:
            if parent1[1].index(q) == length-1:
                if parent1[1][0] in legitimates:
                    a = parent1[1][0]
                else:
                    a = legitimates[0]
            elif parent1[1][parent1[1].index(q)+1] in legitimates:
                a = parent1[1][parent1[1].index(q)+1]
            else:
                a = legitimates[0]

            if parent2[1].index(q) == length-1:
                if parent2[1][0] in legitimates:
                    b = parent2[1][0]
                else:
                    b = legitimates[0]
            elif parent2[1][parent2[1].index(q)+1] in legitimates:
                b = parent2[1][parent2[1].index(q)+1]
            else:
                b = legitimates[0]

            if M[q][a] > M[q][b]:
                child.append(b)
                legitimates.remove(b)
                q = b
            else:
                child.append(a)
                legitimates.remove(a)
                q = a
        for j in range(0, len(child)):
            x = child[j]
            if j < len(child) - 1:
                y = child[j + 1]
            else:
                y = child[0]
            childCost += M[x][y]

        # Introduces a chance of mutation, but only continues with it if it is better than the child without mutation
        r = random.random()
        modedChild = copy.deepcopy(child)
        modCost = childCost + 1
        if r < 0.5:
            modCost = 0
            m = random.randint(0,len(child)-1)
            n = random.randint(0, len(child) - 1)
            c = int(child[m])
            v = int(child[n])
            modedChild[m] = v
            modedChild[n] = c
            for j in range(0, len(modedChild)):
                x = modedChild[j]
                if j < len(modedChild) - 1:
                    y = modedChild[j + 1]
                else:
                    y = modedChild[0]
                modCost += M[x][y]
        if modCost <= childCost:
            newChild = [modCost, modedChild]
        else:
            newChild = [childCost, child]

        genePoolNew.append(newChild)
    genePoolNew = sorted(genePoolNew)
    if genePoolNew[0][0] < bestRoute[0]:
        bestRoute = genePoolNew[0]
    genePool = sorted(genePoolNew)
    print(bestRoute[0], bestRoute[1])
#load file and convert to list
file2 = open("tourAISearchfile012.txt","r+")
fileString2 = file2.read()
fileString2 = fileString2.replace("\n", "").replace("\r","")
fileList2 = []

# One string (one line) created
for char in fileString2:
    if char.isalpha() or char == "=" or char == " ":
        fileString2 = fileString2.replace(char,'')

# dirt and non-numbers (and commas) removed
fileList2 = fileString2.split(",")
# List created
del fileList2[0]
score2 = int(fileList2[1])
del fileList2[0]
print ("score = " + str(score2))
print(bestRoute[0], bestRoute[1])
if bestRoute[0] <= score2:
    file2.truncate(0)
    file2.seek(0)
    out = [str(h) for h in bestRoute[1]]
    file2.write("NAME = AISearchfile012,\nTOURSIZE = 012,\nLENGTH = " + str(bestRoute[0]) + ",\n" + ', '.join(out))
