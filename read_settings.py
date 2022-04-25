import json

nombreJSON = 'config.json'
file = open(nombreJSON, 'r')
data = json.load(file)
file.close()

instancias = data['instancias']
tecnicas = data['tecnicas']

#print(instancias)

key_instancias = list(instancias.keys())
print(key_instancias)
a = key_instancias[1]
print(eval(instancias[a]["hasHeader"]))
