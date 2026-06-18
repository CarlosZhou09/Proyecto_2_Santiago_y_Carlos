"""
Primero se crea la clase del chef y luego en la cocina se crea la parte 
de cambio de chef

como aqui se esta creando prmero la clase del chef, entocnes el la parte
donde interactua con los ingredientes esta vacio
"""

#esta parte de abajo es para senialar la direccion del chef y estableciendolo como variable
ARRIBA = (-1, 0)
ABAJO = (1, 0)
IZQUIERDA = (0, -1)
DERECHA = (0, 1)


class Chef:

    def __init__(self, nombre, fila, columna, color):

        self._nombre = nombre #sera entre chef 1 y chef 2
        self.fila = fila #ubicar su posicion inicial
        self.columna = columna #ubicar su posicion inicial
        self.color = color #establecer el color del chef

        self.direccion = ABAJO

        # Ingrediente que el chef esta sosteniendo (None si no tiene nada).
        self._ingrediente = None

    @property
    def nombre(self):
        return self._nombre

    @property
    def ingrediente(self):
        """Acceso de solo lectura al ingrediente que el chef sostiene."""
        return self._ingrediente


    def tiene_ingrediente(self):
        #retorna True si el chef tiene un ingrediente en las manos
        return self._ingrediente is not None

    def tomar(self, ingrediente):
        """
        El chef toma un ingrediente (de una despensa, de una estacion, etc).
        Solo puede sostener uno a la vez: si ya tiene algo, no se reemplaza.

        Retorna True si logro tomarlo, False si ya tenia las manos ocupadas.
        """
        if self.tiene_ingrediente():
            return False
        self._ingrediente = ingrediente
        return True

    def soltar(self):
        """
        El chef suelta el ingrediente que esta cargando (lo deja en una
        estacion, lo entrega, lo bota en el basurero, etc).

        Retorna el ingrediente soltado, o None si no tenia nada.
        """
        ingrediente = self._ingrediente
        self._ingrediente = None
        return ingrediente


    #MOVIMIENTO
    def mover(self, direccion, celda_libre):
        """
        aqui registra sus movimientos si lo logro o si fue bloqueado
        asi registra si adelante hay un muro o una estacon o si esta en piso normal 
        """
        self.direccion = direccion
        nueva_fila = self.fila + direccion[0]
        nueva_columna = self.columna + direccion[1]

        if celda_libre(nueva_fila, nueva_columna):
            self.fila = nueva_fila
            self.columna = nueva_columna
            return True
        return False

    def celda_frente(self):
        """
        Retorna la coordenada (fila, columna) de la celda que esta justo
        en frente del chef, segun hacia donde esta mirando. Esto es lo
        que usa Cocina para saber con que estacion puede interactuar.
        """
        return (self.fila + self.direccion[0], self.columna + self.direccion[1])


    def __str__(self): #esto es para ver si en las manos no tiene nada
        carga = self._ingrediente if self._ingrediente is not None else "nada"
        return f"{self._nombre} en ({self.fila}, {self.columna}) cargando: {carga}"