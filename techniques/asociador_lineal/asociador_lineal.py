import pandas as pd
import numpy as np

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
 
    return "There is no such Key"


def asociador_lineal(archivo, delimitador=',', hasHeader=None, hasIndex=None):
    """
        archivo (str): Nombre del archivo, con path(opcional)
        delimitador (str, opcional): Separador de los datos. ',' por defecto.
        hasHeader (int, opcional): Numero de fila que contiene el encabezado. 'None' por defecto
        hasIndex (int, opcional): Numero de columna que contiene el nombre de las filas. 'None' por defecto.
    """
    dfArchivo = pd.read_csv(archivo, 
        delimiter=delimitador, 
        header=hasHeader, 
        index_col=hasIndex)

    return(dfArchivo)
    
# Leemos los datos
archivo = "instances/Instancia_clase.csv"
dfArchivo = asociador_lineal(archivo)
datos, clases, clasesSet = [], [], set()

# Separamos los datos de las clases
for i in range(len(dfArchivo)):
    datos.append(list(dfArchivo.iloc[i])[:-1])    
    clases.append(dfArchivo.iloc[i,-1])
    clasesSet.add(dfArchivo.iloc[i, -1])
    # print(datos[i])

# Identificamos las clases
clasesDic = {}
for i, j in enumerate(clasesSet):
    clasesDic[j] = i

# Ciframos los clases
clasesCifradas = []
for i in range(len(clases)):
    a = []
    for j in range(len(clasesSet)):
        a.append(0)
    a[clasesDic[clases[i]]] = 1
    clasesCifradas.append(a)
    print(datos[i], clasesCifradas[i], get_key(clasesDic, clasesDic[clases[i]]))

print("\n")
# Operaciones de matrices con los datos y clases cifrados
# con ayuda de numpy
X = np.array(datos)
Y = np.array(clasesCifradas).T
Xt = X.T

Paso1 = Xt.dot(X)
Paso2 = np.linalg.inv(Paso1)
Xpseudo = X.dot(Paso2)

W = Y.dot(Xpseudo)

print(Xt, "\n\n", Y, "\n\n", W)
    
