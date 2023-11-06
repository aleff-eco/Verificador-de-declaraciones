import sys
import re
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from Interfaz import Ui_Automata  


patrones= [
    (r'^(int\s+[a-zA-Z]\w*\s*=\s*\d+;)\s*$', "Declaracion de variable entera"),
    (r'^(float\s+[a-zA-Z]\w*\s*=\s*\d+\.\d+;)\s*$', "Declaracion de variable flotante"),
    (r'^(string\s+[a-zA-Z]\w*\s*=\s*"[a-zA-Z0-9\s]*";)\s*$', "Declaracion de variable de cadena"),
    (r'^(boolean\s+[a-zA-Z]\w*\s*=\s*(true|false);)\s*$', "Declaracion de variable booleana"),
    #(r'^if\s+[a-zA-Z]\w*\s*(>=|<=|==|<|>)\s*\d+:\s*$', "Declaracion condicional con comparacion"), con o sin argumentos y opcional 'return'"
    
    (r'^if\s+[a-zA-Z]\w*\s*(>=|<=|==|<|>)\s*\d+:\s*C\s*(else:\s*C\s*)?$', "Declaracion condicional con comparacion"),
    (r'^for\s+[a-zA-Z]\w*\s+in\s+[a-zA-Z]\w*:\s*C\s*$', "Declaracion de bucle 'for'"),
    (r'^while\s+[a-zA-Z]\w*\s*(>=|<=|==|<|>)\s*\d+:\s*C$', "Declaracion de bucle 'while'"),
    (r'^def\s+[a-zA-Z]\w*\s*\(\s*([a-zA-Z]\w*\s*(,\s*[a-zA-Z]\w*\s*)*)?\)\s*:\s*C\s*(return\s+[a-zA-Z]\w*\s*;)?$', "Declaracion de funcion"),
    (r'^print\(".+?"\);$', "Instruccion de impresion con texto entre comillas"),
    (r'^print\(.+?\);$', "Instruccion de impresion de una variable" )
]


def validar_declaracion(statement):
    patron_valid = []
    patron_tested= []

    for patron, descripcion in patrones:    
        if re.match(patron, statement):
            patron_valid.append((patron, descripcion))
            break
        else:
            patron_tested.append((patron, descripcion))
    
    if patron_valid:
        return patron_valid, patron_tested
    else:
        return None, patron_tested

class MiVentana(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Automata()
        self.ui.setupUi(self)
        self.ui.send.clicked.connect(self.validar_declaracion)

    def validar_declaracion(self):
        statement = self.ui.input.text()
        patron_valid, patron_tested= validar_declaracion(statement)
        self.ui.i_declaracion.clear()
        self.ui.t_declaracion.clear()
        self.ui.resultado.clear()
        self.ui.patron.clear()
        self.ui.evaluacion.clear()

        if patron_valid:
            for patron, descripcion in patron_valid:
                self.ui.i_declaracion.addItem(statement)
                self.ui.t_declaracion.addItem(descripcion)
                self.ui.resultado.addItem("Es una declaracion valida.")
                self.ui.patron.addItem(patron)
                
            for patron, descripcion in patron_tested:
                self.ui.evaluacion.addItem(f"Descripcion: {descripcion}")
                self.ui.evaluacion.addItem(f"Patron: {patron},")
                self.ui.evaluacion.addItem("")  
        else:
            self.ui.i_declaracion.addItem(statement)
            self.ui.t_declaracion.addItem("Declaracion no valida")
            self.ui.resultado.addItem("Declaracion no valida")
            self.ui.patron.addItem("N/A")
            self.ui.evaluacion.addItem("No coincide con los siguientes patrones:")
            self.ui.evaluacion.addItem("")  

            for patron, descripcion in patron_tested:
                
                self.ui.evaluacion.addItem(f"Descripcion: {descripcion}")
                self.ui.evaluacion.addItem(f"Patron: {patron},")
                self.ui.evaluacion.addItem("")  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec_())
