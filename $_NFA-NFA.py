import queue
f = open("citire.txt")
n = int(f.readline()) #numar stari
alfabet = [x for x in f.readline().split()] #caractere alfabet
q0 = int(f.readline())  #starea initiala
final = {int(x) for x in f.readline().split()} #stari finale
l=[{} for i in range(n)] #nested dict pt matricea de adiacenta
tranzitie = f.readline()
while tranzitie!="":
    (a,b,c)=[x for x in tranzitie.split()]
    if b not in l[int(a)]:
        l[int(a)][b]=set()
    l[int(a)][b].add(int(c))
    tranzitie=f.readline()
coada = queue.Queue(n)
inchdictere = [{x} for x in range(n)]
#pasul 1: calcularea $-inchdicterii
for i in range(n):
    coada.put(i)
    while not coada.empty():
        aux = coada.get()
        if '$'in l[aux]:
            for x in l[aux]['$']:
                if x not in inchdictere[i]:
                    inchdictere[i].add(x)
                    coada.put(x)
nfa = [{} for i in range(n)]
#pasul2: calcularea functiei de tranzitie
for x in alfabet:
    for i in range(n):
        temp=set()
        nfa[i][x]=set()
        for j in inchdictere[i]:
            if x in l[j]:
                temp=temp.union(l[j][x])
        for j in temp:
            nfa[i][x]=nfa[i][x].union(inchdictere[j])
nfa_final=set()
nfa_final=nfa_final.union(final)
#pasul3: calcularea starilor finale si initiale
for i in range(n):
    for x in final:
        if x in inchdictere[i]:
            nfa_final.add(i)
dict={}
lista=[0]*n
#pasul4: eliminarea starilor redundante
for i in range(n):
    for j in range(i+1,n):
        if nfa[i]==nfa[j]:
            if lista[i]==0:
                lista[i]=lista[j]=1
                dict[i]={j} #verificam daca starea doua stari sunt identice
            else:
                for x in dict:
                    if i in dict[x]:
                        dict[x].add(j)
for k in dict:
    for x in range(n):
        for i in alfabet:
            for j in dict[k]:
                if j in nfa[x][i]:
                    nfa[x][i].remove(j) #eliminam una dintre starile care au fost marcate ca fiind identice
                    nfa[x][i].add(k)
k=0
for i in dict:
    for j in dict[i]:
        nfa.remove(nfa[j-k])
        n-=1
        k+=1
for i in range(n):
    for j in alfabet:
        aux = set()
        for x in nfa[i][j]:
            x1 = x
            for a in dict:
                for b in dict[a]:
                    if x>b:
                        x1 -= 1
            aux.add(x1)
        nfa[i][j]=aux
fin = set()
for i in nfa_final:
    x = i
    for a in dict:
        for b in dict[a]:
            if i > b:
                x -= 1
    fin.add(x)
print(nfa)