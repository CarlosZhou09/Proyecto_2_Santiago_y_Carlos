class Estacion:
    """Clase base. Toda estacion ocupa una celda (fila, columna) en la cuadricula."""
 
    def __init__(self, nombre, fila, columna):
        self._nombre = nombre
        self.fila = fila
        self.columna = columna
 
    @property
    def nombre(self):
        return self._nombre
 
    def interactuar(self, chef, cocina):
        """Devuelve un mensaje de texto con el resultado de la interaccion."""
        raise NotImplementedError
 
    # Etiqueta corta para dibujar en pantalla
    def etiqueta(self):
        return "?"
 
 
class Despensa(Estacion):
    """
    Entrega copias ilimitadas de un ingrediente, una a la vez.
    Recibe una 'fabrica': una funcion que crea un ingrediente nuevo.
    """
 
    def __init__(self, nombre, fila, columna, fabrica_ingrediente):
        super().__init__(nombre, fila, columna)
        self._fabrica = fabrica_ingrediente
 
    def interactuar(self, chef, cocina):
        if chef.tiene_ingrediente():
            return "Tienes las manos ocupadas"
        nuevo = self._fabrica()
        chef.tomar(nuevo)
        return f"Tomaste {nuevo.nombre}"
 
    def etiqueta(self):
        return self._nombre[:3].upper()
 
 
class EstacionTrabajo(Estacion):
    """
    Prepara ingredientes (Cocina, Tabla de picar, Freidora).
    `tipo` indica que tipo de preparacion realiza.
    `ingredientes_aceptados` es la lista de categorias que admite.
    """
 
    def __init__(self, nombre, fila, columna, tipo, ingredientes_aceptados):
        super().__init__(nombre, fila, columna)
        self._tipo = tipo
        self.ingredientes_aceptados = list(ingredientes_aceptados)
 
    @property
    def tipo(self):
        return self._tipo
 
    def interactuar(self, chef, cocina):
        ing = chef.ingrediente
        if ing is None:
            return "No traes ningun ingrediente"
        if ing.categoria not in self.ingredientes_aceptados:
            return f"{self._nombre} no acepta {ing.nombre}"
        if ing.esta_listo():
            return f"{ing.nombre} ya esta listo"
        ing.preparar()
        return f"{ing.nombre} ahora esta {ing.estado}"
 
    def etiqueta(self):
        return {"cocina": "COC", "tabla": "TAB", "freidora": "FRE"}.get(self._tipo, "TRB")
 
 
class Basurero(Estacion):
    """Permite botar un ingrediente equivocado para empezar de nuevo."""
 
    def __init__(self, nombre, fila, columna):
        super().__init__(nombre, fila, columna)
 
    def interactuar(self, chef, cocina):
        if not chef.tiene_ingrediente():
            return "No traes nada que botar"
        ing = chef.soltar()
        return f"Botaste {ing.nombre}"
 
    def etiqueta(self):
        return "BAS"