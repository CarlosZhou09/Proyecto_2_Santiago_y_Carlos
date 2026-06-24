"""
cocina.py
---------
Clase Cocina para Crazy Snack Rush TEC.

Es el orquestador central del juego: contiene a los chefs, las estaciones
y las ordenes (via GestorRecetas). Juego (main.py) solo le habla a Cocina;
Cocina se encarga de coordinar todo lo demas.

Dependencias:
  - chef.py              (Carlos)
  - estacion_entrega.py  (Carlos)
  - mapas.py             (Carlos)
  - Estaciones.py        (Santiago) -> Despensa, EstacionTrabajo, Basurero
  - Logica_recetas.py    (Santiago) -> GestorRecetas
  - Ingredientes.py      (Santiago) -> crear_ingrediente
"""

from chef import Chef
from estacion_entrega import EstacionEntrega
from mapas import MAPAS

# Clases de Santiago
from Estaciones import Despensa, EstacionTrabajo, Basurero
from Logica_recetas import GestorRecetas
from Ingredientes import crear_ingrediente


class Cocina:
    """
    Administra todo el estado logico del juego para un escenario dado.
    Juego la crea al cargar un mapa y la actualiza cada frame.
    """

    def __init__(self, clave_mapa):
        """
        Parametros
        ----------
        clave_mapa : str
            Una de las claves de mapas.MAPAS: "burger_bytes", "taco_logic",
            o "gourmet_stack".
        """
        self._clave_mapa = clave_mapa
        self._mapa = MAPAS[clave_mapa]

        self._tiempo = float(self._mapa["tiempo_partida"])
        self._chefs = []
        self._estaciones = []
        self._mapa_estaciones = {}   # (fila, columna) -> Estacion
        self.entrega = None          # referencia rapida a EstacionEntrega

        self._chef_activo = 0        # indice del chef que recibe controles

        # GestorRecetas administra ordenes, timer de recetas y puntaje
        self._gestor = GestorRecetas(self._mapa)

        # Construir chefs y estaciones segun el mapa
        self._construir()

    # ------------------------------------------------------------------
    # Construccion del escenario
    # ------------------------------------------------------------------
    def _construir(self):
        """Lee el diccionario del mapa y crea chefs y estaciones."""

        # Chefs
        for datos in self._mapa["chefs"]:
            chef = Chef(
                datos["nombre"],
                datos["fila"],
                datos["columna"],
                datos["color"]
            )
            self._chefs.append(chef)

        # Estaciones
        for datos in self._mapa["estaciones"]:
            estacion = self._crear_estacion(datos)
            self._agregar_estacion(estacion)
            if datos["tipo"] == "entrega":
                self.entrega = estacion

    def _crear_estacion(self, datos):
        """Fabrica una estacion a partir de su diccionario de configuracion."""
        tipo = datos["tipo"]
        nombre = datos["nombre"]
        fila = datos["fila"]
        columna = datos["columna"]

        if tipo == "despensa":
            clave_ing = datos["ingrediente"]
            fabrica = lambda c=clave_ing: crear_ingrediente(c)
            return Despensa(nombre, fila, columna, fabrica)

        elif tipo == "cocina":
            return EstacionTrabajo(nombre, fila, columna, "cocina", ["proteina"])

        elif tipo == "tabla":
            return EstacionTrabajo(nombre, fila, columna, "tabla", ["vegetal"])

        elif tipo == "freidora":
            return EstacionTrabajo(nombre, fila, columna, "freidora", ["papa"])

        elif tipo == "entrega":
            return EstacionEntrega(nombre, fila, columna)

        elif tipo == "basurero":
            return Basurero(nombre, fila, columna)

        else:
            raise ValueError(f"Tipo de estacion desconocido: {tipo}")

    def _agregar_estacion(self, estacion):
        """Registra la estacion en la lista y en el mapa de coordenadas."""
        self._estaciones.append(estacion)
        self._mapa_estaciones[(estacion.fila, estacion.columna)] = estacion

    # ------------------------------------------------------------------
    # Propiedades (encapsulacion)
    # ------------------------------------------------------------------
    @property
    def tiempo(self):
        return self._tiempo

    @property
    def chefs(self):
        return list(self._chefs)

    @property
    def ordenes(self):
        return self._gestor.ordenes

    @property
    def puntaje(self):
        return self._gestor.puntaje

    @property
    def estaciones(self):
        return list(self._estaciones)

    @property
    def chef_activo(self):
        return self._chefs[self._chef_activo]

    @property
    def nombre_mapa(self):
        return self._mapa["nombre"]

    @property
    def dificultad(self):
        return self._mapa["dificultad"]

    # ------------------------------------------------------------------
    # Control de chefs (TAB)
    # ------------------------------------------------------------------
    def cambiar_chef(self):
        """Cambia el chef activo al otro. Se llama cuando el jugador presiona TAB."""
        self._chef_activo = (self._chef_activo + 1) % len(self._chefs)

    # ------------------------------------------------------------------
    # Movimiento del chef activo (WASD)
    # ------------------------------------------------------------------
    def mover_chef_activo(self, direccion):
        """
        Mueve el chef activo en la direccion indicada, si la celda esta libre.
        direccion: una de las constantes ARRIBA/ABAJO/IZQUIERDA/DERECHA de chef.py
        """
        self._chefs[self._chef_activo].mover(direccion, self._celda_libre)

    def _celda_libre(self, fila, columna):
        """
        Retorna True si la celda (fila, columna) esta libre: no tiene estacion
        y esta dentro de los limites de la cuadricula.
        Se pasa como callable a Chef.mover() para que Chef no conozca el mapa.
        """
        filas = 7
        columnas = 9
        if not (0 <= fila < filas and 0 <= columna < columnas):
            return False
        if (fila, columna) in self._mapa_estaciones:
            return False
        # Tampoco puede ocupar la celda de otro chef
        for i, chef in enumerate(self._chefs):
            if i != self._chef_activo and chef.fila == fila and chef.columna == columna:
                return False
        return True

    # ------------------------------------------------------------------
    # Interaccion (tecla E)
    # ------------------------------------------------------------------
    def interactuar_chef_activo(self):
        """
        El chef activo intenta interactuar con la estacion que tiene enfrente.
        Retorna un string con el resultado (para mostrarlo como mensaje en pantalla).
        Si no hay estacion enfrente, retorna un mensaje indicandolo.
        """
        chef = self._chefs[self._chef_activo]
        fila_f, columna_f = chef.celda_frente()
        estacion = self.estacion_en(fila_f, columna_f)

        if estacion is None:
            return "No hay nada ahi"

        return estacion.interactuar(chef, self)

    # ------------------------------------------------------------------
    # Metodos que EstacionEntrega necesita de Cocina
    # ------------------------------------------------------------------
    def buscar_receta_coincidente(self, platillo):
        """Delega a GestorRecetas. Usado por EstacionEntrega al entregar."""
        return self._gestor.buscar_receta_coincidente(platillo)

    def completar_receta(self, receta):
        """Delega a GestorRecetas. Usado por EstacionEntrega al entregar."""
        return self._gestor.completar_receta(receta)

    # ------------------------------------------------------------------
    # Consultas de mapa
    # ------------------------------------------------------------------
    def estacion_en(self, fila, columna):
        """Retorna la estacion en (fila, columna), o None si no hay ninguna."""
        return self._mapa_estaciones.get((fila, columna))

    # ------------------------------------------------------------------
    # Estado del juego
    # ------------------------------------------------------------------
    def terminado(self):
        """Retorna True si el tiempo de la partida se agoto."""
        return self._tiempo <= 0

    # ------------------------------------------------------------------
    # Actualizacion por frame (llamada desde el bucle principal)
    # ------------------------------------------------------------------
    def actualizar(self, dt):
        """
        Avanza el estado del juego dt segundos.
        Se llama una vez por frame desde Juego.correr() en main.py.

        Hace tres cosas:
          1. Descuenta el tiempo de la partida.
          2. Actualiza GestorRecetas (genera ordenes, aplica penalizaciones).
          3. Si la partida termino, le dice a GestorRecetas que deje de generar.
        """
        if self.terminado():
            return

        self._tiempo -= dt
        if self._tiempo < 0:
            self._tiempo = 0

        # generar=False cuando ya se acabo el tiempo
        self._gestor.actualizar(dt, generar=not self.terminado())