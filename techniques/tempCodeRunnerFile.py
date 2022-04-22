
# for i in range(len(tipos)):
#     print(tipos[i])
#     if(tipos[i] == "float64"):
#         continue
#         columna = dfArchivo[i].to_list()
#         newColumna = discretizador_ewb(columna, 6)
#         dfArchivo.loc[i,] = newColumna
        
#     elif(tipos[i] == "object"):        
#         columna = dfArchivo[i].to_list()
#         newColumna = discretizador_str(columna)
#         print(dfArchivo.iloc[i])
#         #dfA