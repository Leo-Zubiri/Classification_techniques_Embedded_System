import pandas as pd


def leer_dataset(archivo, delimitador=',', hasHeader=None, hasIndex=None):
    """
        archivo (str): Nombre del archivo, con path(opcional) a leer
        delimitador (str, opcional): Separador de los datos. ',' por defecto.
        hasHeader (int, opcional): Numero de fila que contiene el encabezado. 'None' por defecto
        hasIndex (int, opcional): Numero de columna que contiene el nombre de las filas. 'None' por defecto.

    Returns:
        pandas.DataFrame: Contenido del archivo en un objeto DataFrame de la libreria Pandas
    """
    # Leemos los datos
    dfArchivo = pd.read_csv(archivo, 
        delimiter=delimitador, 
        header=hasHeader, 
        index_col=hasIndex)

    return(dfArchivo)


def mapear_dataset(dfArchivo, mapFloat=True, mapStr=True):
    """    
        dfArchivo (pandas.DataFrame): DataFrame con la informacion del archivo
        mapFloat (bool, opcional): Mapear columnas float. 'True' por defecto
        mapStr (bool, opcional): Mapear columnas string. 'True' por defecto

    Returns:
        pandas.DataFrame: DataFrame mapeado
        diccionario: Llaves = Indice Columna: discretizador
    """
    dfAC = dfArchivo.copy()
    tipos = dfAC.dtypes
    discretizador = {}

    #for i, colName in enumerate(tipos)-1:
    for i, head in enumerate(tipos.index):
        if(mapFloat and tipos[head] == "float64"):        
            columna = dfAC[head].to_list()
            intervalos = get_intervalos(columna)
            newColumna, discret = discretizador_ewb(columna, intervalos)            
            dfAC[head] = newColumna
            discretizador[i] = discret
            
        elif(mapStr and tipos[head] == "object"):                
            columna = dfAC[head].to_list()
            newColumna, discret = discretizador_str(columna)
            dfAC[head] = newColumna
            discretizador[i] = discret
        
        else:            
            dicCol = {}
            setCol = set(dfAC[head].to_list())
            for c in setCol:
                dicCol[c] = c

            discretizador[i] = dicCol
        
    return dfAC, discretizador


def get_intervalos(columna):
    columnaSet = set(columna)
    intervalos = len(columnaSet)    
    while(intervalos > 16):
        intervalos = int((intervalos**0.5))
    return intervalos


def discretizador_ewb(columna, intervalos):
    """
        columna (list): Columna con datos float a discretizar
        intervalos (int): Entero que marca la cantidad de intervalos a discretizar
    """
    v_min, v_max= min(columna), max(columna), 
    v_width = round((v_max-v_min)/intervalos, 4)
    
    menor = round(v_min - v_width * 2, 4)
    control = round(v_min + v_width, 4)  

    vectorInt = [menor, control]
    for i in range(1, intervalos-1):
        control = round(control+v_width,4)
        vectorInt.append(control)
    
    mayor = round(control + v_width * 2, 4)
    vectorInt.append(mayor)    

    newCol = []
    for c in columna:
        for i in range(intervalos):
            if(vectorInt[i] <= c and c < vectorInt[i+1]):
                newCol.append(i+1)                
                break
    
    return(newCol, vectorInt)


def discretizador_str(columna):
    columnaSet = set(columna)
    columnaDic = {}
    for d, key in enumerate(columnaSet):
        columnaDic[key] = d + 1
    
    newCol = []
    for c in columna:
        newCol.append(columnaDic[c])
    
    return(newCol, columnaDic)


def discretizar_vp(vp, discretizador, dtipos):
    vpDiscretizado = []
    for d in range(len(dtipos)-1):        
        if(dtipos.iloc[d] == "float64"):
            intervalos = discretizador[d]

            for i in range(len(intervalos)-1):
                if(intervalos[i] <= vp[d] and vp[d] < intervalos[i+1]):
                    vpDiscretizado.append(i+1)                
                    break
        
        elif(dtipos.iloc[d] == "object"):
            diccionario = discretizador[d]            
            vpDiscretizado.append(diccionario[vp[d]])            

        else:
            vpDiscretizado.append(vp[d])
    
    return(vpDiscretizado)


def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
 
    return "No existe esa clave"

# archivo = "../instances/Instancia_wine.csv"
# print(leer_archivo(archivo))
