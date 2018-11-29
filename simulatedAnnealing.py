
'''
    Elliot Jordan
    AI Search
'''
import random as rd
import math


def annealing():
    #load file and convert to list
    file = open("AISearchfile535.txt","r")
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

    nodes = list(range(1, length + 1))
    path = rd.sample(nodes, len(nodes))
    #path = []
    #path.append(1)
    #nodes.remove(1)
    #nextNode = -1
    #q=0
    #while len(path) < length:
    #    best = max(M[1])
    #    for j in nodes:
    #        if M[path[q]][j] < best:
    #            best = M[path[q]][j]
    #            nextNode = j
    #    path.append(nextNode)
    #    nodes.remove(nextNode)
    #    q+=1
    length = len(path)

    cost = 0
    T = 100000

    for j in range(0, length):
        x = path[j]
        if j < len(path) - 1:
            y = path[j + 1]
        else:
            y = path[0]
        cost += M[x][y]

    bestPath = [cost, path]

    while T > 1:

        m = rd.randint(0, length-1)
        n = rd.randint(0, length-1)
        while m==n:
            n = rd.randint(0, length - 1)
        pathNew = path[:]
        pathNew[m] = pathNew[n]
        pathNew[n] = path[m]

        changeCost = 0

        for j in range(0, length):
            x = pathNew[j]
            if j < len(pathNew) - 1:
                y = pathNew[j + 1]
            else:
                y = pathNew[0]
            changeCost += M[x][y]

        change = cost - changeCost
        P = math.e**(change/T)


        if change >= 0:
            cost = changeCost
            path = pathNew[:]
        elif rd.random() < P:
            cost = changeCost
            path = pathNew[:]

        if cost < bestPath[0]:
            bestPath = [cost,path]
        T = 0.9999*T


    #load file and convert to list
    file2 = open("tourAISearchfile535.txt","r+")
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
    print(bestPath[0], bestPath[1])
    if bestPath[0] <= score2:
        file2.truncate(0)
        file2.seek(0)
        out = [str(h) for h in bestPath[1]]
        file2.write("NAME = AISearchfile535,\nTOURSIZE = 535,\nLENGTH = " + str(bestPath[0]) + ",\n" + ', '.join(out))
    return (bestPath[0])

while annealing() > 60000:
    x = 1
