import pandas as pd

# ! Falta depurar el vector problema


def leer_archivo(archivo, delimitador=',', hasHeader=None, hasIndex=None, depurar = True):
    """
        archivo (str): Nombre del archivo, con path(opcional)
        delimitador (str, opcional): Separador de los datos. ',' por defecto.
        hasHeader (int, opcional): Numero de fila que contiene el encabezado. 'None' por defecto
        hasIndex (int, opcional): Numero de columna que contiene el nombre de las filas. 'None' por defecto.
        depurar (bool, opcional): Discretizar columnas flotantes y strings. 'True' por defecto.
    """
    # Leemos los datos
    dfArchivo = pd.read_csv(archivo, 
        delimiter=delimitador, 
        header=hasHeader, 
        index_col=hasIndex)
    
    if(not depurar):
        return dfArchivo

    tipos = dfArchivo.dtypes

    #for i, colName in enumerate(tipos)-1:
    for i in range(len(tipos)-1):    
        if(tipos[i] == "float64"):        
            columna = dfArchivo[i].to_list()
            intervalos = get_intervalos(columna)
            newColumna = discretizador_ewb(columna, intervalos)
            dfArchivo[i] = newColumna
            
        elif(tipos[i] == "object"):                
            columna = dfArchivo[i].to_list()
            newColumna = discretizador_str(columna)
            dfArchivo[i] = newColumna
            #print(dfArchivo[i])
            #print(dfArchivo.iloc[,i])
        
    return dfArchivo


def get_intervalos(datos):
    datosSet = set(datos)
    l = len(datosSet)
    intervalos = int((l**0.5))
    while(intervalos > 16):
        intervalos = int((l**0.5))
    return intervalos

def discretizador_ewb(datos, intervalos):
    """
        datos (list): Lista de la columna a discretizar
        intervalos (int): Entero que marca la cantidad de intervalos a discretizar
    """
    v_min, v_max= min(datos), max(datos), 
    v_width = round((v_max-v_min)/intervalos, 4)
    
    menor = round(v_min - v_width * 2, 4)
    control = round(v_min + v_width, 4)  

    vector = [menor, control]
    for i in range(1, intervalos-1):
        control = round(control+v_width,4)
        vector.append(control)
    
    mayor = round(control + v_width * 2, 4)
    vector.append(mayor)
    #print("Intervalos: {}\nLenVector: {}\n".format(intervalos, len(vector)))

    newDatos = []
    for d in datos:
        for i in range(intervalos):
            if(vector[i] <= d and d < vector[i+1]):
                newDatos.append(i+1)
                #print("{}, {}".format(d, i+1))
                break

    #print("{}, {}".format(len(datos), len(newDatos)))
    return(newDatos)


def discretizador_str(datos):
    datosSet = set(datos)
    datosDic = {}
    for d, key in enumerate(datosSet):
        datosDic[key] = d
    
    newDatos = []
    for d in datos:
        newDatos.append(datosDic[d])
    
    return(newDatos)




# archivo = "../instances/Instancia_iris.csv"
# leer_archivo(archivo)
