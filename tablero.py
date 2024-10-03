import random

class Celda:
    def __init__(self, x, y, tiene_mina):
        self.x = x
        self.y = y
        self.mina = tiene_mina
        self.descubierta = False

    def imprimir(self):
        print(f"Celda en {self.x}, {self.y} con mina? {self.mina}")

    def establecer_mina(self, tiene_mina):
        if self.tiene_mina():
            return False
        else:
            self.mina = tiene_mina
            return True

    def tiene_mina(self):
        return self.mina

    def esta_descubierta(self):
        return self.descubierta

    def set_descubierta(self, descubierta):
        self.descubierta = descubierta

class Tablero:
    def __init__(self, altura, anchura, modo_programador):
        self.altura = altura
        self.anchura = anchura
        self.modo_programador = modo_programador
        self.contenido = [[Celda(x, y, False) for x in range(self.anchura)] for y in range(self.altura)]

    def obtener_representacion_mina(self, x, y):
        c = self.contenido[y][x]
        if c.esta_descubierta() or self.modo_programador:
            if c.tiene_mina():
                return "*"
            else:
                return str(self.minas_cercanas(y, x))
        else:
            return "."

    def minas_cercanas(self, fila, columna):
        conteo = 0
        for m in range(max(0, fila - 1), min(self.altura, fila + 2)):
            for l in range(max(0, columna - 1), min(self.anchura, columna + 2)):
                if self.contenido[m][l].tiene_mina():
                    conteo += 1
        return conteo

    def imprimir(self):
        self.imprimir_encabezado()
        self.imprimir_separador_encabezado()
        for y in range(self.altura):
            print(f"| {y + 1} ", end="")
            for x in range(self.anchura):
                print(f"| {self.obtener_representacion_mina(x, y)} ", end="")
            print("|")
            self.imprimir_separador_filas()

    def imprimir_separador_encabezado(self):
        print("----" * (self.anchura + 1))

    def imprimir_separador_filas(self):
        print("|---" + "+---" * self.anchura + "+")

    def imprimir_encabezado(self):
        self.imprimir_separador_encabezado()
        print("|   ", end="")
        for l in range(self.anchura):
            print(f"| {l + 1} ", end="")
        print("|")

    def colocar_mina(self, x, y):
        return self.contenido[y][x].establecer_mina(True)

    def descubrir(self, x, y):
        self.contenido[y][x].set_descubierta(True)
        return not self.contenido[y][x].tiene_mina()

    def contar_celdas_sin_minas_y_sin_descubrir(self):
        return sum(1 for fila in self.contenido for celda in fila if not celda.esta_descubierta() and not celda.tiene_mina())

class Juego:
    def __init__(self, tablero, cantidad_minas):
        self.tablero = tablero
        self.cantidad_minas = cantidad_minas
        self.colocar_minas_aleatoriamente()

    def colocar_minas_aleatoriamente(self):
        minas_colocadas = 0
        while minas_colocadas < self.cantidad_minas:
            x = random.randint(0, self.tablero.anchura - 1)
            y = random.randint(0, self.tablero.altura - 1)
            if self.tablero.colocar_mina(x, y):
                minas_colocadas += 1

    def solicitar_fila(self):
        return int(input("Ingresa la fila: ")) - 1

    def solicitar_columna(self):
        return int(input("Ingresa la columna: ")) - 1

    def jugador_gana(self):
        return self.tablero.contar_celdas_sin_minas_y_sin_descubrir() == 0

    def iniciar(self):
        while True:
            self.tablero.imprimir()
            fila = self.solicitar_fila()
            columna = self.solicitar_columna()
            if not self.tablero.descubrir(columna, fila):
                print("Perdiste")
                self.tablero.modo_programador = True
                self.tablero.imprimir()
                break
            if self.jugador_gana():
                print("Ganaste")
                self.tablero.modo_programador = True
                self.tablero.imprimir()
                break

if __name__ == "__main__":
    filas = 8
    columnas = 10
    minas = 10
    modo_programador = False
    juego = Juego(Tablero(filas, columnas, modo_programador), minas)
    juego.iniciar()