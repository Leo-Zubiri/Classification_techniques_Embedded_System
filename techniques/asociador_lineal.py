import pandas as pd
import numpy as np
import leer_dataset as lds

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
 
    return "No existe esa clave"

def asociador_lineal(vectorProblema, archivo, delimitador=',', hasHeader=None, hasIndex=None, depurar=True):
    """
        vectorProblema (list): Vector con los 'N' datos requeridos por la instancia elegida
        archivo (str): Nombre del archivo, con path(opcional)
        delimitador (str, opcional): Separador de los datos. ',' por defecto.
        hasHeader (int, opcional): Numero de fila que contiene el encabezado. 'None' por defecto
        hasIndex (int, opcional): Numero de columna que contiene el nombre de las filas. 'None' por defecto.
    """
    # Leemos los datos
    # Usando la nueva funcion del archivo "leer_dataset.py"
    dfArchivo = lds.leer_archivo(archivo, delimitador, hasHeader, hasIndex, depurar)



    datos, clases, clasesSet = [], [], set()

    # Separamos los datos de las clases
    for i in range(len(dfArchivo)):
        datos.append(list(dfArchivo.iloc[i])[:-1])    
        clases.append(dfArchivo.iloc[i,-1])
        clasesSet.add(dfArchivo.iloc[i, -1])
        print(datos[i])

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
        # print(datos[i], clasesCifradas[i], get_key(clasesDic, clasesDic[clases[i]]))

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

    vectorClase = W.dot(vectorProblema)

    indiceClase = list(vectorClase).index(max(vectorClase))
    decisionClase = get_key(clasesDic, indiceClase)
    print("Caso: ",vectorProblema)
    print("Clase: ",decisionClase)        
    
    return(decisionClase)
    

# vectorProblema = [56, 78, 90, 71, 47, 68]
# archivo = "instances/Instancia_clase.csv"

#vectorProblema = [3, 2, 3, 1, 1, 2, 3, 1, 5]
#archivo = "instances/Instancia_cancer.csv"

vectorProblema = [5, 3, 5, 0.3]
archivo = "instances\Instancia_iris.csv"
#archivo = "../instances/Instancia_iris.csv"

# vectorProblema = [12, 1, 2.5, 22, 110, 3.1, 3, 0.32, 1.18, 7.69, 0.50, 2.22, 623]
# archivo = "instances\Instancia_wine.csv"

asociador_lineal(vectorProblema, archivo)
