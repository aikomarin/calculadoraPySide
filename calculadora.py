from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ventana
        self.setWindowTitle('Calculadora')
        self.setFixedSize(235, 235)

        # Layout
        self.layout_principal = QVBoxLayout()
        self.contenedor = QWidget(self)
        self.contenedor.setLayout(self.layout_principal)
        self.setCentralWidget(self.contenedor)

        # Métodos de instancia
        self._crear_area_captura()
        self._crear_botones()
        self._conectar_botones()

    def _crear_area_captura(self):
        self.entrada = QLineEdit()
        self.entrada.setFixedHeight(35)  # Establecer un alto
        self.entrada.setAlignment(Qt.AlignRight)
        self.entrada.setReadOnly(True)
        self.layout_principal.addWidget(self.entrada)

    def _crear_botones(self):
        self.botones = {}
        layout_botones = QGridLayout()
        self.botones = {
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            '/': (0, 3),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '*': (1, 3),
            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '-': (2, 3),
            '0': (3, 0),
            '.': (3, 1),
            'C': (3, 2),
            '+': (3, 3),
            '=': (3, 4)
        }
        for texto_boton, posicion in self.botones.items():
            self.botones[texto_boton] = QPushButton(texto_boton)  # Crear botones con el texto
            self.botones[texto_boton].setFixedSize(40, 40)  # Fijar tamaño de los botones
            layout_botones.addWidget(self.botones[texto_boton], posicion[0], posicion[1])  # Índices de la tupla (F-C)
        self.layout_principal.addLayout(layout_botones)

    def _conectar_botones(self):
        for texto_boton, boton in self.botones.items():
            if texto_boton not in {'=', 'C'}:  # No se aplica con estos botones
                boton.clicked.connect(partial(self._construir_expresion, texto_boton))
                # partial: similar a lambda pero con un parámetro fijo
            self.botones['C'].clicked.connect(self._limpiar_linea_entrada)
            self.botones['='].clicked.connect(self._calcular_resultado)
            self.entrada.returnPressed.connect(self._calcular_resultado)

    def _construir_expresion(self, texto_boton):
        expresion = self.obtener_texto() + texto_boton
        self.actualizar_texto(expresion)

    def obtener_texto(self):
        return self.entrada.text()

    def actualizar_texto(self, texto):
        self.entrada.setText(texto)
        self.entrada.setFocus()

    def _limpiar_linea_entrada(self):
        self.actualizar_texto('')

    def _calcular_resultado(self):
        resultado = self._evaluar_expresion(self.obtener_texto())
        self.actualizar_texto(resultado)

    def _evaluar_expresion(self, expresion):
        try:
            resultado = str(eval(expresion))
        except Exception:
            resultado = 'Error'
        return resultado


if __name__ == '__main__':
    app = QApplication([])
    calculadora = Calculadora()
    calculadora.show()
    app.exec()
