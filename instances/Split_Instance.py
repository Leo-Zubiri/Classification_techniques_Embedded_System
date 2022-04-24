import math
import random

#60/40      70/30       80/20       90/10
#split_types = [.60, .70, .80, .90] 
split_types = [.70] 

archivo = "instances\\Instancia_iris.csv"
trainFileName = "training\\iris_training"+".csv"
testFileName = "test\\iris_test"+".csv"

file = open(archivo)
content_file = file.readlines()

tot_files = len(content_file)
print("Count: ", tot_files)

#Esto ya retorna los archivos xd

backup = []
backup.extend(content_file)
print(backup[0])

for i in range(len(split_types)):
    training = open(trainFileName, "w")
    test = open(testFileName, "w")
    
    random.shuffle(content_file)
    print(backup[0])
    print(content_file[0])

    t_training  = math.ceil(tot_files * split_types[i])
    print("Training Cases: " , t_training)

    for j in range(t_training):
        training.write(content_file[j]) 

    for j in range(t_training, tot_files):
        test.write(content_file[j])        

    training.close()
    test.close()

    content_file = []
    content_file.extend(backup)