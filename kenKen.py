from csp import *
from itertools import product
import time

_PLUS = 1
_MINUS = 2
_MULT = 3
_DIV = 4


#Both of these functions help us find the domains of PLUS cliques

#Returns all the possible partitions
def partition(number, sizeOfCLique, dims):
    #print("BEGIN")
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition(number - x, sizeOfCLique, dims):
            #found = tuple((x, ) + y)
            answer.add(tuple((x,) + y))
            #print(answer)
            #if(len(found) == sizeOfCLique) and (max(found) <= dims):
              #  answer.add(tuple((x, ) + y))
    #print(max(list(answer)))
    return answer

#Keep and return the partitions that are of sizeOfClique and all their values <= dims
def findPartitionOfNumb(number, sizeOfCLique, dims):
    res = partition(number, sizeOfCLique, dims)
    res.remove((number, ))

    toBeRemoved = set()
    for i in res:
        if len(i) != sizeOfCLique or max(i) > dims:
            toBeRemoved.add(i)
    #print(toBeRemoved)
    finalRes = res.difference(toBeRemoved)
    #print(res)
    return list(finalRes)


#Finds the domain of MULT cliques
def findFactorsOfNumber(number, sizeOfCLique, dims):
    permuts = list(product(list(range(1, dims + 1)), repeat=sizeOfCLique))
    retRes = []
    for i in permuts:
        mult = 1
        # print(i)
        for j in i:
            mult *= j
        if mult == number:
            retRes.append(i)
    return retRes

#I assume that division and subtraction will have a sizeOfClique == 2

#Finds the domain of DIV cliques
def findDivisionDomain(number, dims):
    retList = []
    for i in range(1, dims + 1):
        for j in range(1, dims + 1):
            if i / j == number or j / i == number:
                retList.append((i, j))
    return retList

#Finds the domain of SUBTRACT cliques
def findSubstractionDomain(number, dims):
    retList = []
    for i in range(1, dims + 1):
        for j in range(1, dims + 1):
            if abs(i - j) == number:
                retList.append((i, j))
    return retList


def getRowNeighs(point, cols):
    n = set()
    for i in range(0, cols):
        if i != point[1]:
            n.add((point[0], i))
    return n

def getColNeighs(point, rows):
    n = set()
    for i in range(0, rows):
        if i != point[0]:
            n.add((i, point[1]))
    return n

#Scans the input clique to find if it is a PLUS, MULT, DIV, SUBTRACT clique
def findOp(str):
    if '+' in str:
        return _PLUS
    elif '-' in str:
        return _MINUS
    elif '*' in str:
        return _MULT
    elif '/' in str:
        return _DIV
    else:
        print("Failed to read operator")
        return -1

#Scans the input to find the points that belong in a clique
def findPoints(str, dims):
    returnPoints = []
    ptsStr = str.split('|')[0]
    pts = ptsStr.split(',')
    for i in pts:
        returnPoints.append((int(i) // dims, int(i) % dims))
    result = re.findall(r'\d+', str.split('|')[1])
    return [returnPoints, int(result[0])]




#Struct that helps us create the domains and neighbors of a clique
class Clique:
    def __init__(self, str, dims):
        self.op = findOp(str)
        self.points, self.res = findPoints(str, dims)

#Finds the object clique that point belongs
def findWhichClique(point, cliques):
    for whichCliq in cliques:
        for whichPoint in whichCliq.points:
            if whichPoint == point:
                return whichCliq

#Finds the key of the clique that point belongs
def findWhichCliqueKey(point, cliques):
    for whichCliq in range(len(cliques)):
        for whichPoint in cliques[whichCliq].points:
            if whichPoint == point:
                return whichCliq

#cl = Clique("0,6|+11", 6)

#Get neighbors of point
def getPointNeighs(n, cliques):
    neighs = {}
    for i in range(0, n):
        for j in range(0, n):
            rowColNeighs = getColNeighs((i, j), n).union(getRowNeighs((i, j), n))
            rowColNeighs.add(findWhichCliqueKey((i,j), cliques))
            #print(rowColNeighs)
            neighs[(i, j)] = rowColNeighs
    return neighs

#Get neighbors of clique
def getCliqueNeighs(cliques):
    retDict = {}
    for i in range(len(cliques)):
        cliqNeigh = set()
        for j in cliques[i].points:
            cliqNeigh.add(j)
        retDict[i] = cliqNeigh
    return retDict

#Create the domains of both points and cliques
def kenKenDomains(n, cliques):
    dicts = {}
    #Points domains
    for i in range(0, n):
        for j in range(0, n):
            dicts[(i,j)] = list(range(1, n + 1))

    #Clique domains
    for c in range(len(cliques)):
        if cliques[c].op == _PLUS:
            dicts[c] = findPartitionOfNumb(cliques[c].res, len(cliques[c].points), n)
        elif cliques[c].op == _MINUS:
            dicts[c] = findSubstractionDomain(cliques[c].res, n)
        elif cliques[c].op == _MULT:
            dicts[c] = findFactorsOfNumber(cliques[c].res, len(cliques[c].points), n)
        elif cliques[c].op == _DIV:
            dicts[c] = findDivisionDomain(cliques[c].res, n)
    return dicts



#Basic assumptions:
#   1)No single participant cliques allowed
#   2)Substraction and division cliques can have exactly 2 participants
class KenKen(CSP):
    def __init__(self, n, str):

        self.dims = n
        self.cliques = []
        self.conflicts = 0
        #Input read
        for i in str.split(';'):
            self.cliques.append(Clique(i, n))

        #Prepare domains and neighbors
        self.domains = kenKenDomains(n, self.cliques)
        self.neighbors = {**getPointNeighs(n, self.cliques), **getCliqueNeighs(self.cliques)}

        CSP.__init__(self, None, self.domains, self.neighbors, self.kekKenConstraints)



    def display(self, assignment):
        for i in range(self.dims):
            for j in range(self.dims):
                print(assignment.get((i, j)), end='')
                print("|", end='')
            print()

    def kekKenConstraints(self, A, a, B, b):
        # Case row or col neigbors (both points)

        if isinstance(A, int) or isinstance(B, int):
            if(isinstance(A, int)):
                point = B
                valuePoint = b
                whichCliq = A
                valueCliq = a
            else:
                point = A
                valuePoint = a
                whichCliq = B
                valueCliq = b

            cliqNeighs= self.neighbors[whichCliq]

            #Find rank of point in clique
            whichRank = -1
            for i in range(len(cliqNeighs)):
                if list(cliqNeighs)[i] == point:
                    whichRank = i
            if whichRank == -1:
                print("UNEXPECTED, whichRank was never initialised")

            #Case: value does NOT appear in correct place of the cliq domain
            if valuePoint != valueCliq[whichRank]:
                self.conflicts += 1
                return False
            # Case: value appears in correct place of the clique domain
            else:
                return True
        #Case: Both neigbors are points (just check if their values are different
        elif len(A) == 2 and len(B) == 2:
            if a != b:
                return True
            else:
                self.conflicts += 1
                return False
        else:
            print("UNEXPECTED ERROR")


cliques6_expert = "0,6|+11;1,2|/2;3,9|*20;7,8|-3;4,5,11,17|*6;12,13,18,19|*240;14,15|*6;10,16|/3;" \
           "20,26|*6;24,25|*6;21,27,28|+7;22,23|*30;29,35|+9;30,31,32|+8;33,34|/2"

cliques3_easy = "0,3|/3;1,2,4|*4;6,7|+5;5,8|-2"

cliques4_medium = "0,1|-3;2,3,7|+8;4,8,12|*6;5,6|-3;9,10|/2;13,14|-1;11,15|-3"

cliques5_hard = "0,5|-1;1,2|-4;3,4|-1;6,7|/2;8,9|*20;10,11,12|+10;13,18|/2;14,19|+7;" \
                "15,20,21|+7;16,17|-1;22,23,24|+9"

cliques7_master = "0,1|/3;2,3,10|+13;4,5|*15;6,13|+11;7,14|+3;8,15|-1;9,16,22,23|*144;" \
                  "11,12|-2;17,24|*28;18,19|-5;25,26|-1;20,27|/3;21,28|-3;29,30,31|+13;32,38,39,45,46|+17;" \
                  "35,42|*15;36,37|-6;43,44|-4;33,40|-3;34,41|-3;47,48|-1"

#KenKen class requires the clique string (above), and the number of rows, columns
dims = 4
problem = cliques4_medium

k = KenKen(dims, problem)
start_time = time.time()
backtracking_search(k)
print(">>>BT | Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

k = KenKen(dims, problem)
start_time = time.time()
backtracking_search(k, select_unassigned_variable=mrv)
print(">>>BT + MRV| Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

k = KenKen(dims, problem)
start_time = time.time()
backtracking_search(k, inference=forward_checking)
print(">>>BT + FC| Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

k = KenKen(dims, problem)
start_time = time.time()
backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)
print(">>>BT + MRV + FC| Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

k = KenKen(dims, problem)
start_time = time.time()
backtracking_search(k, inference=mac)
print(">>>BT + MAC| Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

# k = KenKen(dims, problem)
# start_time = time.time()
# min_conflicts(k)
# print(">>>Min conflicts | Time = " + str((time.time() - start_time)) + " | Conflicts = " + str(k.conflicts) + " | Assigns = " + str(k.nassigns))

print()
print(">>>Result Grid")
k.display(k.infer_assignment())


