path = "Discretizador_EWB/"     # Para Yochua
nombre_archivo = "wine.csv"

#archivo = open("iris_completa.csv")
archivo = open(path + nombre_archivo)
contenido = archivo.readlines()
#############################################################################################
instancia = []
for i in contenido:
    instancia.append(i.split(","))
encabezados = instancia[0]
del instancia[0] 
#############################################################################################
###GRUPOS A GENERAR
v_K = 5    # Pagina de referencia comparativa ->>>>  https://orange.readthedocs.io/en/latest/reference/rst/Orange.feature.discretization.html#Orange.feature.discretization.Discretization
#############################################################################################
intervalos = []
for index_atributo in range(len(instancia[0])-1):
    auxiliar = []
    for index_registro in range(len(instancia)):
        auxiliar.append(float(instancia[index_registro][index_atributo]))
    v_max = max(auxiliar)
    v_min = min(auxiliar)
    v_width = round((v_max-v_min)/v_K,4)
    ######################################################################
    # print("Atributo analizado:" , encabezados[index_atributo])
    # print("min: ", v_min)
    # print("max: ", v_max)    
    # print("width: ", v_width)

    #!##################################################################### 
    # IMPRESION DE INTERVALOS

    # control  = round(v_min+v_width,4)
    # temp = ["<" + str(control)]
    # for j in range(1,v_K-1):
    #     s = "[" + str(control) + ", "
    #     control = round(control+v_width,4)
    #     s += str(control) + ")"
    #     temp.append(s)
    # temp.append(">=" + str(control))
    
    # intervalos.append(temp)
    # auxiliar.clear()
    

    #!##################################################################### 
    # PRIMERA FORMA, un vector de matrices con datos menores y mayores

    # menor = round(v_min - v_width * 2, 4)
    # control = round(v_min + v_width, 4)

    # matriz = [[menor, control]]
    # for j in range(1, v_K-1):
    #     vector = [control]
    #     control = round(control + v_width, 4)
    #     vector.append(control)
    #     matriz.append(vector)

    # mayor = round(control + v_width * 2, 4)
    # matriz.append([control, mayor])

    # intervalos.append(matriz)
    # auxiliar.clear()

    

    #!##################################################################### 
    # # SEGUNDA FORMA, un vector de vectores con los intervalos
    # # for i in range(len(vector)-1):
    # #     menor = vector[i]
    # #     mayor = vector[i+1]
      

    menor = round(v_min - v_width * 2, 4)
    control = round(v_min + v_width, 4)  

    vector = [menor, control]
    for j in range(1, v_K-1):
        control = round(control+v_width,4)
        vector.append(control)
    
    mayor = round(control + v_width * 2, 4)
    vector.append(mayor)
    
    intervalos.append(vector)
    auxiliar.clear()

#!############################################################################################

for i in intervalos:
    print(i)

print()
for i in range(len(intervalos[0])-1):
    print("[{}, {})".format(intervalos[0][i], intervalos[0][i+1]))