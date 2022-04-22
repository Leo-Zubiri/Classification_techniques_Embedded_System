import pandas as pd

#archivo = "instances/Instancia_cancer.csv"
archivo = "instances/Instancia_clase.csv"
#archivo = "instances/Instancia_iris.csv"
#archivo = "instances/Instancia_wine.csv"

df = pd.read_csv(archivo, header=None)
print(df)
print()

print(df.dtypes)
print()
print(df.dtypes)

print(df.describe())


minmax = list(zip(df.min(), df.max()))

# print("Min - Max  :  len= ", len(minmax))
# #print(minmax)
# for i in minmax:
#     print(i)