# x = [1, 1, 1]
# zeros = len(x)
# b = bin(2**zeros)
# print(b)

# a = bin(b>>1)
# print(a)


# import numpy as np
# a = [
#     [0, 0, 1],
#     [0, 0, 1],
#     [1, 0, 0],
#     [0, 1, 0],
#     [1, 0, 0]
# ]

# b = np.array(a)
# print(b,"\n\n", b.T)


import pandas as pd

#archivo = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"

archivo = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

dfArchivo = pd.read_csv(archivo, header=None) 
print(dfArchivo, "\n")  

tipos = dfArchivo.dtypes 
for i, head in enumerate(tipos.index):
    columna = dfArchivo[head].to_list() 
    print("{}\n\n{}\n\n{}\n\n".format(i,columna, dfArchivo[head]))
    