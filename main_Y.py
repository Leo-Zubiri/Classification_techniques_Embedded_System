import sys
import json
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
# Modulo/clase arduino
import arduinoWind as ard
from techniques.knn_2 import knn as knn
from techniques.asociador_lineal import asociador_lineal as asolin
from techniques.naive_bayes import naive_bayes as naibay
import techniques.mapeador as mapea

qtCreatorFile = "main.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btnArduino.clicked.connect(self.conectar)
        self.btnIdentificar.clicked.connect(self.identificar)
        
        self.instancias, self.tecnicas, self.keyInst = self.read_yeison() 
        self.key = 0         
        self.instancia = self.instancias[self.keyInst[self.key]]                       

        archivo, delim, head, index = list(self.instancia.values())       
        self.dfDataset = mapea.leer_dataset(archivo, delim, eval(head), eval(index))      
        self.dfDsMap, self.discretizador = mapea.mapear_dataset(self.dfDataset)           
        
        self.tecnica = list(self.tecnicas.items())[0][0]   
        self.funcion = self.tecnicas[self.tecnica]
        
        self.cbInstancia.currentIndexChanged.connect(self.setInstancia)
        self.cbTecnica.currentIndexChanged.connect(self.setTecnica)

        # New Window
        self.ardApp  = QtWidgets.QApplication(sys.argv)
        self.ardWindow = ard.MyApp()
       
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execTimer)
        self.timer.start(10)


    def read_yeison(self):
        nombreJSON = 'config.json'
        file = open(nombreJSON, 'r')
        data = json.load(file)
        file.close()

        instancias = data['instancias']
        tecnicas = data['tecnicas']
        key_instancias = list(instancias.keys())
        self.cbInstancia.addItems(instancias.keys())
        self.cbTecnica.addItems(tecnicas.keys())

        return instancias, tecnicas, key_instancias


    def conectar(self):
        self.ardWindow.show()
    

    def setInstancia(self):                
        self.key = self.cbInstancia.currentIndex()
        self.instancia = self.instancias[self.keyInst[self.key]] 

        archivo, delim, head, index = list(self.instancia.values())       
        self.dfDataset = mapea.leer_dataset(archivo, delim, eval(head), eval(index))      
        self.dfDsMap, self.discretizador = mapea.mapear_dataset(self.dfDataset) 
        print(self.dfDataset, "\n") 

        
    def setTecnica(self):        
        index = self.cbTecnica.currentIndex()
        self.tecnica = str(self.cbTecnica.itemText(index))
        self.funcion = self.tecnicas[self.tecnica]


    def identificar(self):
        print("\n----- {} -----".format(self.tecnica))
        text = (self.instancia_ard.text())
        vp = list(map(int, text.split(',')))            
        vpMap = self.mapearVP(vp)
        func = "{}({},{})".format(
            "eval(self.funcion)", "vpMap", "self.dfDsMap")             
        decision = eval(func)
        lon = len(self.discretizador) - 1
        decisionKey = mapea.get_key(self.discretizador[lon], decision)
        print("Decision: ", decisionKey)
        print()
        
        # ! ------------------------------------------
        # ! ------------------------------------------
        # Se envia el dato "decision" al arduino
        # ! ------------------------------------------
        # ! ------------------------------------------
        

    def mapearVP(self, vpArduino):
        #print("\nvp INO:      ",vpArduino)
        mins = self.dfDataset.min().to_list()
        maxs = self.dfDataset.max().to_list()
        
        vp = list(map(lambda x, y, z: round(x*(z-y)/1023+y, 4), vpArduino, mins, maxs ))
        #print("vp INO map:  ",vp)
        
        
        dtipos = self.dfDataset.dtypes
        vpMap = mapea.discretizar_vp(vp, self.discretizador, dtipos)
        #print("vp mapeado:  ",vpMap)
        #print()       
        
        return vpMap


    # Timer para el Python
    def execTimer(self):
        lect = self.ardWindow.getLectura()
        
        if(lect == "Desconectado"):
            self.instancia_ard.setText(lect)
            return
        else:
            lon = self.dfDataset.shape[1] - 1
            lect = lect.split(",")
            vp, vLect = [], []
            if len(lect) >= lon:
                vLect = [int(x) for x in lect]
                vLect = vLect[:lon]               
                vp = self.mapearVP(vLect)

            #print("Es aqui",lect)
            self.instancia_ard.setText(self.listToStr(vLect))
            self.instancia_ard_2.setText(self.listToStr(vp))      

    # Estos dos... el primero no se que era xd, y el segundo me daba error al cerrar la ventana xddd
    # def agregar(self):
    #     dato = self.txt_arduino.text()
    #     self.list_datos.addItem(dato)        
    #     self.txt_arduino.setText("")
    #     self.txt_arduino.setFocus() 


    def listToStr(self, lista):
        listaString = str(lista)
        lon = len(listaString)
        cadena = str(listaString[1: lon-1])
        return cadena


    def closeEvent(self, event):
        self.ardWindow.close()
        if self.timer.isActive():
            self.timer.stop()
        sys.exit(self.ardApp.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
