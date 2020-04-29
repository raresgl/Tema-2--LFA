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
    l[int(a)][b]=int(c)
    tranzitie=f.readline()
adiacenta = [[True]*x for x in range(n)]
nefinal = {x for x in range(n)} - final
#pasul1: determinarea starilor echivalente
for x in final:
    for y in nefinal:
        adiacenta[max(x,y)][min(x,y)]=False
ok = True
while ok:
    ok = False
    for i in range(n):
        for j in range(i):
            for x in alfabet:
                a = l[i][x]
                b = l[j][x]
                if a != b and adiacenta[max(a,b)][min(a,b)] is False:
                    ok = adiacenta[i][j]
                    adiacenta[i][j] = False

aux = [x for x in range(n-1,-1,-1)]
#pasul2: gruparea starilor echivalente si calcularea functiei de tranzitie
new = []
for x in aux:
    dict = {x}
    for j in range(len(adiacenta[x])):
        if adiacenta[x][j]:
            dict.add(j)
            aux.remove(j)
    new.append(dict)

new = new[::-1]
m = len(new) #lungimea noului dfa(min)
dfa_min = [{} for i in range(m)]
for i in range(m):
    for y in alfabet:
        x = next(iter(new[i]))
        x = l[x][y]
        for j in range(m):
            if x in new[j]:
                dfa_min[i][y] = j
#pasul3: calcularea starilor finale si initiale
for i in range(m):
    if q0 in new[i]:
        q0_min = i
        break
final_min = set()
for i in range(m):
    if final.intersection(new[i]):
        final_min.add(i)
coada = queue.Queue(m)
#pasul4: eliminarea starilor dead-end
for x in range(m):
    coada.put(x)
    bool_array = [False] * m
    bool_array[x] = True
    while not coada.empty():
        while not coada.empty():
            i = coada.get()
            for j in alfabet:
                if j in dfa_min[i]:
                    if dfa_min[i][j] in final_min:
                        break
                    if not bool_array[dfa_min[i][j]]:
                        coada.put(dfa_min[i][j])
                        bool_array[dfa_min[i][j]] = True
            else:
                dfa_min = dfa_min[:i] + dfa_min[i + 1:]
                k = i
                for i in range(len(dfa_min)):
                    for j in alfabet:
                        if j in dfa_min[i] and dfa_min[i][j]==k:
                            dfa_min[i].pop(j)
                        if j in dfa_min[i] and dfa_min[i][j] > k:
                            dfa_min[i][j] -= 1
#pasul5: eliminarea starilor neaccesibile
coada = queue.Queue(m)
coada.put(q0)
bool_array = [False]*m
bool_array[q0] = True
while not coada.empty():
    i = coada.get()
    for j in alfabet:
        if j in dfa_min[i] and dfa_min[i][j]:
            if not bool_array[dfa_min[i][j]]:
                coada.put(dfa_min[i][j])
                bool_array[dfa_min[i][j]] = True
for i in range(m):
    if not bool_array[i]:
        dfa_min = dfa_min[:i] + dfa_min[i + 1:]
        for x in range(len(dfa_min)):
            for y in alfabet:
                if y in dfa_min[x] and dfa_min[x][y] and dfa_min[x][y]>i:
                    dfa_min[x][y] -= 1
print(dfa_min)