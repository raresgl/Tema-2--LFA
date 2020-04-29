import queue
f = open("citire.txt")
n = int(f.readline()) #numar stari
alfabet = [x for x in f.readline().split()] #caractere alfabet
q0 = int(f.readline())  #starea initiala
final = {int(x) for x in f.readline().split()} #stari finale
l=[{} for i in range(n)] #nested dict pt matricea de adiacenta
for i in range(n):
    for x in alfabet:
        l[i][x]=set()
tranzitie = f.readline()
while tranzitie!="":
    (a,b,c)=[x for x in tranzitie.split()]
    if b not in l[int(a)]:
        l[int(a)][b]=set()
    l[int(a)][b].add(int(c))
    tranzitie=f.readline()
coada=queue.Queue()
temp = set()
for x in alfabet:
    temp = temp.union(l[q0][x])
coada.put(tuple(temp))
lista = [tuple([q0]),tuple(temp)]
#pasul1: eliminarea nedeterminismului
while not coada.empty():
    a = coada.get()
    for y in alfabet:
        temp = set()
        for x in a:
            temp = temp.union(l[x][y])
        temp = tuple(temp)
        if temp not in lista:
            coada.put(temp)
            lista.append(temp)
dfa_final=[] #multimea starilor finale din noul dfa
#pasul2: calcularea starilor finale
for i in range(len(lista)):
    for x in lista[i]:
        if x in final:
            dfa_final.append(i)
dfa = [{} for i in range(len(lista))]
#pasul3: redenumirea starilor
for i in range(len(lista)):
    for x in alfabet:
        aux = set()
        for k in lista[i]:
            aux = aux.union(l[k][x])
        if aux!=set():
            dfa[i][x]=lista.index(tuple(aux))
print(dfa)