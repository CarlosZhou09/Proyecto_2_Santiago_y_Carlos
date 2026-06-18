class Receta:

    # Constantes de diseño (definidas en el documento de planteamiento).
    PUNTOS_POR_INGREDIENTE = 20
    TIEMPO_BASE = 20
    TIEMPO_POR_INGREDIENTE = 15
    TIEMPO_PENALIZACION = 8  # cada cuantos segundos de retraso se parte el puntaje a la mitad

    def __init__(self, nombre, requeridos):

        self._nombre = nombre #cada receta por ejemplo hamburguesa, ensalada, etc
        self._requeridos = list(requeridos)

        cantidad = len(self._requeridos)
        self._puntos_originales = self.PUNTOS_POR_INGREDIENTE * cantidad
        self._puntos_actuales = self._puntos_originales

        self._tiempo_maximo = self.TIEMPO_BASE + self.TIEMPO_POR_INGREDIENTE * cantidad
        self._tiempo_restante = float(self._tiempo_maximo)

        # cuenta cuantas veces ya se penalizo desde que el tiempo llego a 0,
        # para saber cuando toca la siguiente penalizacion (cada 8s extra).
        self._penalizaciones_aplicadas = 0

    #lo de encapsulacion
    @property
    def nombre(self):
        return self._nombre

    @property
    def requeridos(self):
        return list(self._requeridos)

    @property
    def puntos_actuales(self):
        return self._puntos_actuales

    @property
    def puntos_originales(self):
        return self._puntos_originales

    @property
    def tiempo_restante(self):
        return self._tiempo_restante

    @property
    def tiempo_maximo(self):
        return self._tiempo_maximo


    def comparar_receta(self, colocados):
        #esto es para que se vea como estan los ingredients ya colocados
        #en la estacion 
        # en esta parteno importa en que orden esten colocados los ingredientes
        #solo si estan
       
        if len(colocados) != len(self._requeridos):
            return False

        claves_colocadas = sorted(ing.clave() for ing in colocados)
        claves_requeridas = sorted(self._requeridos)
        return claves_colocadas == claves_requeridas


    def actualizar(self, dt):
        #especifica que el timer va en segundos y siempre va a ir en regresiva 

        #por cada vez que se acabe el tiempo, entra en estado de tiempo extra con la mitad de puntos

        self._tiempo_restante -= dt

        if self._tiempo_restante > 0:
            return self._puntos_actuales

        # Tiempo extra transcurrido desde que se llego a 0.
        tiempo_extra = -self._tiempo_restante
        penalizaciones_que_deberian_estar = int(tiempo_extra // self.TIEMPO_PENALIZACION) + 1

        # Solo aplicamos las penalizaciones nuevas que falten (puede que
        # actualizar() se llame varias veces por segundo, no queremos
        # partir el puntaje mas de lo que corresponde por el tiempo real).
        nuevas = penalizaciones_que_deberian_estar - self._penalizaciones_aplicadas
        for _ in range(max(0, nuevas)):
            self._puntos_actuales //= 2
            self._penalizaciones_aplicadas += 1

        if self._puntos_actuales <= 0:
            self._puntos_actuales = 0

        return self._puntos_actuales

    def expirada(self):
        #True si la receta ya perdio todos sus puntos y debe eliminarse
        return self._puntos_actuales <= 0


    def resumen(self):
        #Linea corta para mostrar en el panel de ordenes de la interfaz.
        ingredientes = ", ".join(nombre for nombre, _estado in self._requeridos)
        return f"{self._nombre}: {ingredientes} | {self._puntos_actuales}pts | {self._tiempo_restante:.0f}s"
    
    def __str__(self):
        return self.resumen()