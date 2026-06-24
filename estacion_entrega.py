"""
estacion_entrega.py
--------------------
Clase EstacionEntrega para Crazy Snack Rush TEC.

Hereda de Estacion (definida por Santiago en Estaciones.py) y sigue el mismo
contrato que el resto de estaciones: interactuar(chef, cocina) siempre
retorna un string con el resultado, para que Cocina lo muestre como mensaje
de feedback en pantalla.

Como funciona en el juego: el chef va depositando ingredientes ya preparados
uno por uno en esta estacion (solo puede cargar uno a la vez). Cada vez que
suelta uno, la estacion revisa si el "platillo" acumulado hasta el momento
ya coincide con alguna receta activa. Si coincide, se entrega automaticamente
y se limpia la estacion para la siguiente orden.

IMPORTANTE: esta clase no decide el puntaje ni busca en la lista de ordenes
por su cuenta. Eso es responsabilidad de GestorRecetas (Santiago), al que
Cocina le debe dar acceso. EstacionEntrega solo le pasa la lista de
ingredientes acumulados a cocina, y cocina es quien pregunta:
"oye GestorRecetas, esto que tengo, hace match con alguna receta?"
"""

from estaciones import Estacion


class EstacionEntrega(Estacion):
    """Punto donde el chef deposita ingredientes para completar una receta."""

    def __init__(self, nombre, fila, columna):
        super().__init__(nombre, fila, columna)
        self._platillo = []  # ingredientes acumulados, en el orden en que se depositaron

    @property
    def platillo(self):
        """Acceso de solo lectura a los ingredientes depositados hasta ahora."""
        return list(self._platillo)

    def limpiar(self):
        """Vacia la estacion. Se usa despues de una entrega exitosa, o si
        el jugador quiere reiniciar un platillo que iba mal."""
        self._platillo = []

    def interactuar(self, chef, cocina):
        """
        El chef deposita el ingrediente que trae cargado.

        Flujo:
          1. Si el chef no trae nada, no hay nada que hacer.
          2. Se agrega el ingrediente al platillo acumulado.
          3. Se le pregunta a cocina si el platillo actual coincide con
             alguna receta activa (cocina delega esto a GestorRecetas).
          4. Si coincide: se entrega, se suman los puntos, se limpia la
             estacion para la siguiente orden.
          5. Si no coincide: el ingrediente se queda esperando a que el
             chef traiga el resto de lo que falta.
        """
        if not chef.tiene_ingrediente():
            return "No traes ningun ingrediente para entregar"

        ingrediente = chef.soltar()
        self._platillo.append(ingrediente)

        receta_completada = cocina.buscar_receta_coincidente(self._platillo)

        if receta_completada is not None:
            puntos = cocina.completar_receta(receta_completada)
            self.limpiar()
            return f"Entregaste {receta_completada.nombre}! +{puntos} puntos"

        return f"Colocaste {ingrediente.nombre}, faltan mas ingredientes"

    def etiqueta(self):
        return "ENT"