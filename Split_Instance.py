import math
import random

#60/40      70/30       80/20       90/10
split_types = [.60, .70, .80, .90] 

file = open("Instancia_wine.csv")
content_file = file.readlines()

tot_files = len(content_file)
print("Count: ", tot_files)

#Esto ya retorna los archivos xd

backup = []
backup.extend(content_file)
print(backup[0])
# Creo que puedes... poner la otra diagonal asi solita sin problemas '/'
# La otra vez se puso mamonsito y no agarraba por eso me voy a lo seguro
# LEL, yo siempre lo hago con la otra :V che piton 
# yayaya entendi el codigo

for i in range(len(split_types)):
    training = open("PracticaClase\\wine_training"+ str(split_types[i]*100) +".csv", "w")
    test = open("PracticaClase\\wine_test"+ str(split_types[i]*100) +".csv", "w")
    
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