#CS 583 Project 1 - MS Apriori Algorithm 
#Contributors: Ayush and Kashyap

import sys

T = []
MS = {} 
illegal = []
must = []
phi=0.0
slist=dict()
count = {}
tail = {}
F=dict()
L=list()
C=dict()
C[1]=list()
F[1]=list()

SC = {}
TC = {}


para=str()


def readInput():
    ''' reads the input transactions from the file '''
    global T,para
    file_name = sys.argv[1]
    para+=sys.argv[2]
    f = open(file_name,'r')

    for line in f.readlines():
        transaction = line.strip().replace('{','').replace('}','').split(',')
        transaction = [int(x) for x in transaction if x != None and x != '']
        T.append(transaction)

    f.close()


def readParams():
    global MS,phi,illegal,must,para
    ''' reads parameters from the file '''
    f = open(para,'r')
    for line in f.readlines():
        
        if line.find("MIS") != -1:
            temp = line.strip().replace('MIS','').replace('(','').replace(')','').split('=')
            MS[int(temp[0])] = float(temp[1])        
        
        if line.find("SDC") != -1:
            phi= float(line.replace(' ','').rstrip().split('=')[1])

        if line.find("cannot_be_together") != -1:
            cannot = line.strip().replace('cannot_be_together','').replace(':','').replace('{','').split('},')

            for i in cannot: 
                grp = i.strip().replace('}','').split(',')
                grp = [int(x) for x in grp if x != None and x != '']
                illegal.append(grp)

        if line.find("must-have") != -1:
            have = line.strip().replace('must-have','').replace(':','').split('or')
            must = [int(x) for x in have if x != None and x != '']

        f.close()


readInput()

readParams()

MS_sort=sorted(MS.keys(), key=lambda x: MS[x])    #List of items sorted according to their MIS values


def initP():
    global MS_sort,T,slist,count,L,F,MS
    i_chk=0
    for I in MS_sort:
        sup_count=0
        for t in T:
            if I in t:
                sup_count+=1

        slist[I]=float(sup_count)/len(T)
        count[I]=sup_count

        if i_chk==0:
            if slist[I]>=MS[I]:
                L.append(I)
                i_chk=I
        else:
            if slist[I]>=MS[i_chk]:
                L.append(I)

    for l in L:
        if slist[l]>=MS[l]:
            F[1].append(l)


initP()


def L2_cand():
    global C,L,slist,MS,phi
    chk=0
    C[2]=list()

    for l in L:
        if slist[l]>=MS[l]:
            temp=L[L.index(l)+1:len(L)]

            for h in temp:
                if slist[h]>=MS[l] and abs(slist[h]-slist[l])<=phi:
                    C[2].append([l,h])


from operator import ne #'not equal to' operatior
def MScandidate_gen(F, phi,k): #pass F[k-1] and phi to this function 
    global C

    C[k] = []
    for f1 in F:
        F1 = F.copy()
        F1.remove(f1)
        for f2 in F1:
            if not any(map(ne,f1[:-1],f2[:-1])) and f1[-1]<f2[-1] and abs(slist[f1[-1]] - slist[f2[-1]]) <= phi:
                c = f1.copy()
                c.append(f2[-1]) #forms the candidate
                C[k].append(c) #appends it to k
                for i in range(0,len(c)):
                    s = c.copy()
                    s.remove(s[i])
                    if c[0] in s or MS[c[2]] == MS[c[1]]:
                        if s not in F:
                            C[k].remove(c)
                            break 

def findFrequent(k):
    global F, SC, count, TC 
    F[k] = []
    for c in C[k]:
        scount = 0
        tcount = 0
        for t in T:
            if set(c) <= set(t): #checks if the c is containe in t
                scount+=1
            if set(c[1:]) <= set(t):
                tcount+=1
        SC[tuple(c)] = scount/len(T)
        count[tuple(c)] = scount
        TC[tuple(c)] = tcount/len(T)
        tail[tuple(c)] = tcount
        
    for c in C[k]: 
        if SC[tuple(c)] >= MS[c[0]]:
            F[k].append(c)

def main():
    k = 2
    while True:
        if k == 2:
            L2_cand()
        else:
            MScandidate_gen(F[k-1],phi,k)

        findFrequent(k)
        
        if F[k] == []:
            break
        k+=1
    

main()

def mustHave():
    global must,F
    newF = []
    for f in F:
        if f == 1:
            for i in F[f]:
                for m in must:
                    if m == i:
                        newF.append(i)
                        break
            F[f] = newF
            newF = []
        else:            
            for i in F[f]:
                for m in must:
                    if m in i:
                        newF.append(i)
                        break
            F[f] = newF
            newF = []

if(must != []):
    mustHave()

def cantbe():
    global F
    k=2
    removeF = []
    while F.get(k) != None and F.get(k) != []:
        for f in F[k]:
            for c in illegal:
                if set(c) <= set(f):
                    removeF.append(f)
                    break
        F[k] = [e for e in F[k] if e not in removeF]
        removeF = []
        k+=1
        
if(illegal != []):
    cantbe()

def fileoutput():
    global F,count,tail 
    k = 2
    file = open("output.txt","w") 
    
    if F.get(1) != [] and F.get(1) != None:
        file.write("Frequent 1-itemsets\n\n")
        print("Frequent 1-itemsets\n\n")
        for fi1 in F[1]:    
            file.write('\t' + str(count[fi1]) + ' : {' + str(fi1) + '}\n')
            print('\t' + str(count[fi1]) + ' : {' + str(fi1) + '}\n')
        file.write("\n\tTotal number of frequent 1-itemsets = " + str(len(F[1])) + "\n\n\n")
        print("\n\tTotal number of frequent 1-itemsets = " + str(len(F[1])) + "\n\n\n")
    while F.get(k) != None and F.get(k) != []:
        file.write("Frequent " + str(k) + "-itemsets\n\n")
        print("Frequent " + str(k) + "-itemsets\n\n")
        for fi in F[k]:   
            csi = ", ".join(map(str,fi))
            file.write('\t' + str(count[tuple(fi)]) + ' : {' + csi + '}\n')
            file.write('Tailcount = ' + str(tail[tuple(fi)]) + "\n")
            print('\t' + str(count[tuple(fi)]) + ' : {' + csi + '}\n')
            print('Tailcount = ' + str(tail[tuple(fi)]) + "\n")
        file.write("\n\tTotal number of frequent " + str(k) + "-itemsets = " + str(len(F[k])) + "\n\n\n")
        print("\n\tTotal number of frequent " + str(k) + "-itemsets = " + str(len(F[k])) + "\n\n\n")
        k+=1
    
    file.write('....')
    file.close() 

fileoutput()

