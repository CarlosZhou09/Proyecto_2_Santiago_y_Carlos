"""
mapas.py
--------
Definicion de los 3 escenarios de Crazy Snack Rush TEC.

Cada mapa es un diccionario con:
  - nombre         : nombre visible del escenario.
  - dificultad     : texto descriptivo.
  - tiempo_partida : duracion total de la partida en segundos.
  - intervalo_generacion : cada cuantos segundos aparece una orden nueva.
  - max_ordenes    : cuantas ordenes pueden estar activas a la vez.
  - recetas        : lista de claves de RECETAS (en GestorRecetas) disponibles.
  - chefs          : posiciones y colores iniciales de los 2 chefs.
  - estaciones     : lista de estaciones con su tipo y posicion en la cuadricula.

La cuadricula es de 9 columnas x 7 filas (indices 0-8 y 0-6).
Las celdas del borde son paredes/estaciones; el interior es el area de movimiento.
"""

MAPAS = {

    # ------------------------------------------------------------------
    # MAPA 1 - Burger Bytes (Hamburgueseria · Facil)
    # Recetas: Papas Fritas, Hamburguesa Clasica, Hot Dog
    # Tiempo: 180s | Spawn: 25s | Max ordenes: 3
    # ------------------------------------------------------------------
    "burger_bytes": {
        "nombre": "Burger Bytes",
        "dificultad": "Facil",
        "tiempo_partida": 180,
        "intervalo_generacion": 25,
        "max_ordenes": 3,
        "recetas": ["papas_fritas", "hamburguesa_clasica", "hot_dog"],

        # Chefs: posicion inicial (fila, columna) y color RGB
        "chefs": [
            {"nombre": "Chef 1", "fila": 3, "columna": 3, "color": (100, 180, 255)},
            {"nombre": "Chef 2", "fila": 3, "columna": 5, "color": (255, 160, 80)},
        ],

        # Estaciones: tipo, nombre visible, fila, columna
        # Tipos: "despensa", "cocina", "tabla", "freidora", "entrega", "basurero"
        "estaciones": [
            # Despensas (fila superior)
            {"tipo": "despensa", "nombre": "Pan",      "fila": 0, "columna": 1, "ingrediente": "pan"},
            {"tipo": "despensa", "nombre": "Carne",    "fila": 0, "columna": 3, "ingrediente": "carne"},
            {"tipo": "despensa", "nombre": "Salchicha","fila": 0, "columna": 5, "ingrediente": "salchicha"},
            {"tipo": "despensa", "nombre": "Papa",     "fila": 0, "columna": 7, "ingrediente": "papa"},

            # Estaciones de trabajo (fila inferior)
            {"tipo": "cocina",   "nombre": "Cocina",   "fila": 6, "columna": 2, "ingrediente": None},
            {"tipo": "freidora", "nombre": "Freidora", "fila": 6, "columna": 5, "ingrediente": None},

            # Entrega y basurero (lados)
            {"tipo": "entrega",  "nombre": "Entrega",  "fila": 3, "columna": 8, "ingrediente": None},
            {"tipo": "basurero", "nombre": "Basurero", "fila": 6, "columna": 8, "ingrediente": None},
        ],
    },

    # ------------------------------------------------------------------
    # MAPA 2 - Taco Logic (Taqueria · Medio)
    # Recetas: Taco de Pollo, Taco de Carne, Taco Supremo
    # Tiempo: 210s | Spawn: 18s | Max ordenes: 4
    # ------------------------------------------------------------------
    "taco_logic": {
        "nombre": "Taco Logic",
        "dificultad": "Medio",
        "tiempo_partida": 210,
        "intervalo_generacion": 18,
        "max_ordenes": 4,
        "recetas": ["taco_pollo", "taco_carne", "taco_supremo"],

        "chefs": [
            {"nombre": "Chef 1", "fila": 3, "columna": 2, "color": (100, 180, 255)},
            {"nombre": "Chef 2", "fila": 3, "columna": 6, "color": (255, 160, 80)},
        ],

        "estaciones": [
            # Despensas
            {"tipo": "despensa", "nombre": "Tortilla", "fila": 0, "columna": 1, "ingrediente": "tortilla"},
            {"tipo": "despensa", "nombre": "Pollo",    "fila": 0, "columna": 3, "ingrediente": "pollo"},
            {"tipo": "despensa", "nombre": "Carne",    "fila": 0, "columna": 5, "ingrediente": "carne"},
            {"tipo": "despensa", "nombre": "Tomate",   "fila": 0, "columna": 7, "ingrediente": "tomate"},
            {"tipo": "despensa", "nombre": "Cebolla",  "fila": 6, "columna": 1, "ingrediente": "cebolla"},
            {"tipo": "despensa", "nombre": "Lechuga",  "fila": 6, "columna": 3, "ingrediente": "lechuga"},

            # Estaciones de trabajo
            {"tipo": "cocina",   "nombre": "Cocina",   "fila": 0, "columna": 8, "ingrediente": None},
            {"tipo": "tabla",    "nombre": "Tabla",    "fila": 6, "columna": 6, "ingrediente": None},

            # Entrega y basurero
            {"tipo": "entrega",  "nombre": "Entrega",  "fila": 3, "columna": 8, "ingrediente": None},
            {"tipo": "basurero", "nombre": "Basurero", "fila": 6, "columna": 8, "ingrediente": None},
        ],
    },

    # ------------------------------------------------------------------
    # MAPA 3 - Gourmet Stack (Restaurante · Dificil)
    # Recetas: Combo de Pescado, Hamburguesa Gourmet, Plato Fuerte, Mega Combo
    # Tiempo: 240s | Spawn: 14s | Max ordenes: 5
    # ------------------------------------------------------------------
    "gourmet_stack": {
        "nombre": "Gourmet Stack",
        "dificultad": "Dificil",
        "tiempo_partida": 240,
        "intervalo_generacion": 14,
        "max_ordenes": 5,
        "recetas": ["combo_pescado", "hamburguesa_gourmet", "plato_fuerte", "mega_combo"],

        "chefs": [
            {"nombre": "Chef 1", "fila": 2, "columna": 2, "color": (100, 180, 255)},
            {"nombre": "Chef 2", "fila": 4, "columna": 6, "color": (255, 160, 80)},
        ],

        "estaciones": [
            # Despensas
            {"tipo": "despensa", "nombre": "Pan",     "fila": 0, "columna": 1, "ingrediente": "pan"},
            {"tipo": "despensa", "nombre": "Carne",   "fila": 0, "columna": 3, "ingrediente": "carne"},
            {"tipo": "despensa", "nombre": "Pescado", "fila": 0, "columna": 5, "ingrediente": "pescado"},
            {"tipo": "despensa", "nombre": "Pollo",   "fila": 0, "columna": 7, "ingrediente": "pollo"},
            {"tipo": "despensa", "nombre": "Lechuga", "fila": 6, "columna": 1, "ingrediente": "lechuga"},
            {"tipo": "despensa", "nombre": "Tomate",  "fila": 6, "columna": 3, "ingrediente": "tomate"},
            {"tipo": "despensa", "nombre": "Cebolla", "fila": 6, "columna": 5, "ingrediente": "cebolla"},
            {"tipo": "despensa", "nombre": "Papa",    "fila": 6, "columna": 7, "ingrediente": "papa"},

            # Estaciones de trabajo
            {"tipo": "cocina",   "nombre": "Cocina",   "fila": 0, "columna": 8, "ingrediente": None},
            {"tipo": "tabla",    "nombre": "Tabla",    "fila": 3, "columna": 0, "ingrediente": None},
            {"tipo": "freidora", "nombre": "Freidora", "fila": 6, "columna": 8, "ingrediente": None},

            # Entrega y basurero
            {"tipo": "entrega",  "nombre": "Entrega",  "fila": 2, "columna": 8, "ingrediente": None},
            {"tipo": "basurero", "nombre": "Basurero", "fila": 4, "columna": 8, "ingrediente": None},
        ],
    },
}

# Orden de los mapas para cargarlos con teclas 1, 2, 3
ORDEN_MAPAS = ["burger_bytes", "taco_logic", "gourmet_stack"]