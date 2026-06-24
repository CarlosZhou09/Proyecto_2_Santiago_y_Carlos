import random
from receta import Receta #le corresponde a Carlos Receta
from Ingredientes import crear_ingrediente   
# Definicion de recetas
# clave = (nombre visible, [ingredientes que lleva])
RECETAS = {
    "papas_fritas":        ("Papas Fritas",        ["papa"]),
    "hamburguesa_clasica": ("Hamburguesa Clasica", ["pan", "carne"]),
    "hot_dog":             ("Hot Dog",             ["pan", "salchicha"]),
    "taco_pollo":          ("Taco de Pollo",       ["tortilla", "pollo", "lechuga"]),
    "taco_carne":          ("Taco de Carne",       ["tortilla", "carne", "cebolla"]),
    "taco_supremo":        ("Taco Supremo",        ["tortilla", "carne", "tomate", "cebolla"]),
    "combo_pescado":       ("Combo de Pescado",    ["pan", "pescado", "lechuga"]),
    "hamburguesa_gourmet": ("Hamburguesa Gourmet", ["pan", "carne", "lechuga", "tomate"]),
    "plato_fuerte":        ("Plato Fuerte",        ["pollo", "papa", "tomate", "cebolla"]),
    "mega_combo":          ("Mega Combo",          ["pan", "carne", "papa", "tomate"]),
}

class GestorRecetas:
    #Administra las ordenes activas, su tiempo, su penalizacion y el puntaje.
 
    def __init__(self, mapa):
        """ mapa: el diccionario de un escenario (configuracion.MAPAS["mapa_1"], etc.).
              De ahi saca: que recetas pueden salir, cada cuanto aparecen,
              y cuantas pueden estar activas a la vez (perillas de dificultad). """
        self._mapa = mapa
        self._ordenes = []        # lista de Receta activas (sin entregar)
        self._puntaje = 0         # puntaje del jugador
 
        # Perillas de dificultad que vienen del mapa
        self._intervalo = mapa["intervalo_generacion"]
        self._max_ordenes = mapa["max_ordenes"]
        self._temporizador = 0.0  # 0 => genera una orden de inmediato al iniciar
 

    # ENCAPSULACION (solo lectura desde afuera)
    @property
    def ordenes(self):
        return list(self._ordenes)
 
    @property
    def puntaje(self):
        return self._puntaje
 
    @property
    def max_ordenes(self):
        return self._max_ordenes
 
    # 1. GENERACION ALEATORIA DE RECETAS
    def _construir_receta(self, clave):
        """Crea una Receta a partir de su clave en configuracion.RECETAS."""
        nombre, claves_ing = RECETAS[clave]
        requeridos = []
        for clave_ing in claves_ing:
            molde = crear_ingrediente(clave_ing)
            # cada requerido es (nombre_visible, estado_en_que_debe_estar)
            requeridos.append((molde.nombre, molde.estado_objetivo()))
        return Receta(nombre, requeridos)
 
    def generar_receta(self):
        """Devuelve una receta ALEATORIA del repertorio del mapa actual."""
        clave = random.choice(self._mapa["recetas"])
        return self._construir_receta(clave)
 
    # 3. SISTEMA DE PUNTUACION (al entregar)
    def buscar_receta_coincidente(self, platillo):
        """
        Devuelve la primera orden activa cuyos ingredientes coincidan con el
        'platillo' (lista de ingredientes ya preparados), o None si ninguna.
        """
        for receta in self._ordenes:
            if receta.comparar_receta(platillo):
                return receta
        return None
 
    def completar_receta(self, receta):
        """Suma los puntos ACTUALES de la receta y la quita de las ordenes."""
        puntos = receta.puntos_actuales
        self._puntaje += puntos
        if receta in self._ordenes:
            self._ordenes.remove(receta)
        return puntos
 
    def intentar_entregar(self, platillo):
        """
        Atajo para mi compañero: recibe el platillo armado, busca si coincide
        con alguna orden y la entrega. Devuelve los puntos ganados, o None si
        el platillo no corresponde a ninguna orden activa.
        """
        receta = self.buscar_receta_coincidente(platillo)
        if receta is None:
            return None
        return self.completar_receta(receta)

    # 2. TIMER + PENALIZACION  (y generacion continua)

    def actualizar(self, dt, generar=True):
        """
        Avanza la logica de recetas `dt` segundos. Hace tres cosas:
          - genera ordenes nuevas cuando toca (si `generar` es True),
          - corre el cronometro de cada receta y aplica la penalizacion,
          - elimina las recetas que llegaron a 0 y RESTA sus puntos originales.
 
        `generar` permite a mi compañero apagar la generacion cuando la partida
        ya termino (para que no sigan apareciendo ordenes).
        """
        # --- generacion de ordenes ---
        self._temporizador -= dt
        necesita_orden = len(self._ordenes) == 0  # siempre debe haber al menos una
        if (self._temporizador <= 0 or necesita_orden) and generar:
            if len(self._ordenes) < self._max_ordenes:
                self._ordenes.append(self.generar_receta())
            self._temporizador = self._intervalo
 
        # timer + penalizacion de cada receta 
        expiradas = []
        for receta in self._ordenes:
            receta.actualizar(dt)          # baja su tiempo y parte sus puntos
            if receta.expirada():          # llego a 0 puntos
                expiradas.append(receta)
 
        # recetas vencidas: se eliminan y restan sus puntos ORIGINALES 
        for receta in expiradas:
            self._ordenes.remove(receta)
            self._puntaje = max(0, self._puntaje - receta.puntos_originales)
 
    # Utilidad para reiniciar sin crear un objeto nuevo (opcional)
    def reiniciar(self):
        self._ordenes.clear()
        self._puntaje = 0
        self._temporizador = 0.0