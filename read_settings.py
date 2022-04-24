import json
 
nombreJSON = 'settings.json'
file = open('settings.json', 'r')
data = json.load(file)
file.close()

instancias = data['instancias']
tecnicas = data['tecnicas']

print(instancias)
print(tecnicas)



