class Ingrediente:
    """Clase base abstracta. No se instancia directamente."""
 
    # Cada subclase define a que categoria pertenece.
    # Las estaciones de trabajo usan esta categoria para decidir
    # si aceptan o no el ingrediente.
    categoria = "generico"
 
    def __init__(self, nombre, estado_inicial):
        self._nombre = nombre
        self._estado = estado_inicial
 
    # Encapsulacion: lectura controlada
    @property
    def nombre(self):
        return self._nombre
 
    @property
    def estado(self):
        return self._estado
 
    # Metodos polimorficos (cada subclase los redefine) 
    def estacion_requerida(self):
        """Tipo de estacion necesaria para prepararlo. None si no necesita."""
        raise NotImplementedError
 
    def estado_objetivo(self):
        """Estado final que debe tener para considerarse listo."""
        raise NotImplementedError
 
    def esta_listo(self):
        """True si el ingrediente ya esta preparado."""
        return self._estado == self.estado_objetivo()
 
    def preparar(self):
        """Cambia el estado del ingrediente a su estado objetivo."""
        self._estado = self.estado_objetivo()
 
    # ----- Utilidades -----
    def igual_que(self, otro):
        """Dos ingredientes son equivalentes si tienen el mismo nombre y estado."""
        return self._nombre == otro.nombre and self._estado == otro.estado
 
    def clave(self):
        """Identidad (nombre, estado) usada para comparar recetas."""
        return (self._nombre, self._estado)
 
    def __str__(self):
        return f"{self._nombre} ({self._estado})"
 
 
class Proteina(Ingrediente):
    """Carne, pollo, pescado, salchicha. Se cocinan en la Cocina (sarten)."""
 
    categoria = "proteina"
 
    def __init__(self, nombre):
        super().__init__(nombre, "crudo")
        self._cocinada = False  # atributo COCINADA del enunciado
 
    @property
    def cocinada(self):
        return self._cocinada
 
    def estacion_requerida(self):
        return "cocina"
 
    def estado_objetivo(self):
        return "cocinado"
 
    def preparar(self):
        super().preparar()       # estado a "cocinado"
        self._cocinada = True
 
 
class Vegetal(Ingrediente):
    """Vegetales y frutas. Se preparan en la Tabla de picar."""
 
    categoria = "vegetal"
 
    def __init__(self, nombre):
        super().__init__(nombre, "entero")
 
    def estacion_requerida(self):
        return "tabla"
 
    def estado_objetivo(self):
        return "picado"
 
 
class Papa(Ingrediente):
    """Papa. Se prepara en la Freidora (papas fritas)."""
 
    categoria = "papa"
 
    def __init__(self, nombre="Papa"):
        super().__init__(nombre, "cruda")
 
    def estacion_requerida(self):
        return "freidora"
 
    def estado_objetivo(self):
        return "frita"
 
 
class PanBase(Ingrediente):
    """Panes y bases (pan, tortilla). No requieren preparacion: ya vienen listos."""
 
    categoria = "base"
 
    def __init__(self, nombre):
        super().__init__(nombre, "listo")
 
    def estacion_requerida(self):
        return None
 
    def estado_objetivo(self):
        return "listo"
 
    def esta_listo(self):
        return True  # siempre listo
    
# Fabrica de ingredientes 
# Convierte una clave de texto (ej. "carne") en el objeto correcto.
INGREDIENTES = {
    "pan":       lambda: PanBase("Pan"),
    "tortilla":  lambda: PanBase("Tortilla"),
    "carne":     lambda: Proteina("Carne"),
    "pollo":     lambda: Proteina("Pollo"),
    "pescado":   lambda: Proteina("Pescado"),
    "salchicha": lambda: Proteina("Salchicha"),
    "lechuga":   lambda: Vegetal("Lechuga"),
    "tomate":    lambda: Vegetal("Tomate"),
    "cebolla":   lambda: Vegetal("Cebolla"),
    "papa":      lambda: Papa("Papa"),
}

def crear_ingrediente(clave):
    return INGREDIENTES[clave]()