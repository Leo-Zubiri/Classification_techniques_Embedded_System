import copy

def unpack_str(nombreArchivo, varSplit):
    archivo = open(nombreArchivo, 'r', encoding='utf-8')
    dataFile = archivo.read().split("\n")
    archivo.close()
    if(dataFile[-1] == ''):
        dataFile.pop()
    
    info = [i.split(varSplit) for i in dataFile]

    return info

# ! ----------------------------------------------------------------------------------

path = "naive_bayes/"   # Opcional, puedes quitarlo y mas abajo tambien, solo pa Yochua uwu
nombreArchivo = "prueba_nb_Y.txt"
varSplit = "\t"
# SOLO funcionara poniendo los datos como STRING, y escritos de la misma manera en la del archivo
# NO es posible ponerlo como numeros debido a la aleatoriedad de los conjuntos
caso = ["Soleado", "Frío", "Alta", "Fuerte"]
caso = ["", "", "", ""]

data = unpack_str(path + nombreArchivo, varSplit)
#data = unpack_str(nombreArchivo, varSplit)
totalCasos = len(data)
vector_conj = []
vector_dic = []

# ! ----------------------------------------------------------------------------------
# Obtenemos los vectores de conjuntos y diccionarios

for i in range(len(data[0])):
    conjunto = set()
    for j in range(len(data)):
        conjunto.add(data[j][i])

    vector_conj.append(conjunto)
    
    dic = {key:info for info, key in enumerate(conjunto)}    
    vector_dic.append(dic)

    # Traducimos el dataset a numeros (key)
    for j in range(len(data)):
        data[j][i] = dic.get(data[j][i])

print("-"*10, "Informacion traduciada a numeros", "-"*10)
for i in data:
    print(i)
print()
print(vector_dic[-1])
print()

# ! ----------------------------------------------------------------------------------

# Vector contador de decisiones de cada atributo
contDecisiones = []
# Vector con las decisiones
decisiones = [0 for i in range(len(vector_conj[-1]))]

# Llenamos el vector 'contDecisiones' con ceros y sus correspondientes vectores
for i in vector_conj:    
    aux = []
    for j in i:
        aux.append(decisiones.copy())
    
    contDecisiones.append(aux)

contDecisiones.pop() # Eliminamos las decisiones

# Contamos todas las decisiones
for i in range(len(data)):
    respuesta = data[i][-1]
    decisiones[respuesta] += 1
    for j in range(len(data[i])-1):
        contDecisiones[j][data[i][j]][respuesta] += 1

print("-"*10, "Decisiones contadas", "-"*10)
for i in contDecisiones:
    print(i)
print()

# ! -----------------------------------------------------------------------------------

# Creamos una copia de las decisiones para obtener las probabilidades
# (Solo nos importa copiar la estructura)
# (podemos sobreescribir "contDecisiones")
probabilidades = copy.deepcopy(contDecisiones)
probDecision = [round(i/totalCasos,4) for i in decisiones]

for i in range(len(probabilidades)):
    for j in range(len(probabilidades[i])):
        for k in range(len(decisiones)):
            probabilidades[i][j][k] = round(contDecisiones[i][j][k]/decisiones[k],4)

print("-"*10,"Probabilidades","-"*10)
for i in probabilidades:
    print(i)
print()

print("-"*10,"Decisiones y su probabilidad","-"*10)
print(decisiones)
print(probDecision)
print()

# ! ----------------------------------------------------------------------------------
# Resolvemos ahora el caso
# Llenamos de 1 para luego ser multiplicadas por las probabilidades obtenidas
probCaso = [1 for i in decisiones]
for k in range(len(probCaso)):
    probCaso[k] *= probDecision[k]
    for i in range(len(caso)):
        # Obtenemos el indice del caso dentro de nuestro vector diccionario
        j = vector_dic[i].get(caso[i])
        
        probCaso[k] *= probabilidades[i][j][k]
    probCaso[k] = round(probCaso[k], 4)

decisionCaso = -1
auxProb = -1
# Buscamos la mayor decision
for i in range(len(probCaso)):
    if(probCaso[i] > auxProb):
        auxProb = probCaso[i]
        decisionCaso = i

print("-"*10,"Resolucion del caso","-"*10)
print("Caso: ", caso)
print("                  ", vector_conj[-1])
print("Prob de Decision: ", probCaso)
print("Decision tomada:  ", list(vector_dic[-1].keys())[decisionCaso])
print()


        

