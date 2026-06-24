"""
interfaz_juego.py
-----------------
Funciones de dibujo del tablero principal para Crazy Snack Rush TEC.

Dibuja:
  - El tablero cuadriculado (fondo, celdas, paredes)
  - Las estaciones en sus celdas (con etiqueta y color segun tipo)
  - Los dos chefs (con su color y la inicial del ingrediente que cargan)
  - HUD superior: tiempo de partida y puntaje
  - Mensajes de feedback (ej. "Tomaste Pan", "Entregaste Hamburguesa!")

Este archivo trabaja junto con Interfaz.py de Santiago, que ya tiene:
  - dibujar_panel_ordenes()  -> panel lateral derecho de ordenes activas
  - dibujar_fin_juego()      -> pantalla de fin con puntaje final
  - Los colores COLOR_FONDO, COLOR_PARED, COLOR_PISO, etc.

main.py importa ambos archivos y los usa en el bucle principal.
"""

import pygame

# -----------------------------------------------------------------------
# Dimensiones (deben coincidir con main.py)
# -----------------------------------------------------------------------
ANCHO_VENTANA = 1280
ALTO_VENTANA  = 720
TAMANO_CELDA  = 100          # cada celda del tablero mide 100x100 px
FILAS         = 7
COLUMNAS      = 9
ANCHO_TABLERO = COLUMNAS * TAMANO_CELDA   # 900 px
ALTO_TABLERO  = FILAS    * TAMANO_CELDA   # 700 px
X_TABLERO     = 0           # el tablero empieza en el borde izquierdo
Y_TABLERO     = 20          # deja 20px arriba para el HUD de tiempo/puntaje

# -----------------------------------------------------------------------
# Colores propios de este archivo
# (los del panel de ordenes viven en Interfaz.py de Santiago)
# -----------------------------------------------------------------------
COLOR_FONDO        = (28,  30,  38)
COLOR_PARED        = (38,  40,  52)
COLOR_PISO         = (52,  56,  70)
COLOR_LINEA        = (65,  68,  85)
COLOR_TEXTO        = (235, 235, 245)
COLOR_TEXTO_TENUE  = (160, 165, 180)
COLOR_OK           = (110, 210, 130)
COLOR_ALERTA       = (235, 110, 110)

# Colores por tipo de estacion
COLOR_ESTACION = {
    "despensa": (70,  130, 180),   # azul acero
    "cocina":   (200,  80,  60),   # rojo/naranja (fuego)
    "tabla":    (100, 160,  80),   # verde (vegetal)
    "freidora": (200, 160,  70),   # amarillo/dorado
    "entrega":  (150,  80, 200),   # morado
    "basurero": (100, 100, 100),   # gris
}

# -----------------------------------------------------------------------
# Utilidades internas
# -----------------------------------------------------------------------
def _rect_celda(fila, columna):
    """Retorna el pygame.Rect de la celda (fila, columna) en pantalla."""
    x = X_TABLERO + columna * TAMANO_CELDA
    y = Y_TABLERO + fila    * TAMANO_CELDA
    return pygame.Rect(x, y, TAMANO_CELDA, TAMANO_CELDA)


def _texto(superficie, texto, fuente, color, cx, cy):
    """Dibuja texto centrado en (cx, cy)."""
    sup = fuente.render(str(texto), True, color)
    rect = sup.get_rect(center=(cx, cy))
    superficie.blit(sup, rect)


def _tipo_estacion(estacion):
    """
    Intenta determinar el tipo de estacion a partir de su clase o etiqueta,
    para poder asignarle el color correcto sin depender de un atributo 'tipo'
    que no todas las subclases tienen.
    """
    etiqueta = estacion.etiqueta()
    mapeo = {
        "ENT": "entrega",
        "BAS": "basurero",
        "COC": "cocina",
        "TAB": "tabla",
        "FRE": "freidora",
    }
    if etiqueta in mapeo:
        return mapeo[etiqueta]
    # Las despensas tienen etiquetas variables (primeras 3 letras del nombre)
    return "despensa"


# -----------------------------------------------------------------------
# Funciones publicas de dibujo
# -----------------------------------------------------------------------
def dibujar_fondo(superficie):
    """Rellena el fondo completo de la ventana."""
    superficie.fill(COLOR_FONDO)


def dibujar_tablero(superficie):
    """
    Dibuja la cuadricula del tablero: fondo de piso para cada celda
    y lineas de separacion.
    """
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            rect = _rect_celda(fila, columna)
            pygame.draw.rect(superficie, COLOR_PISO, rect)
            pygame.draw.rect(superficie, COLOR_LINEA, rect, 1)


def dibujar_estaciones(superficie, estaciones, fuente):
    """
    Dibuja cada estacion en su celda con su color de tipo y su etiqueta.

    superficie : pantalla pygame
    estaciones : lista de objetos Estacion (cocina.estaciones)
    fuente     : fuente pequeña para la etiqueta
    """
    for est in estaciones:
        rect = _rect_celda(est.fila, est.columna)
        tipo = _tipo_estacion(est)
        color = COLOR_ESTACION.get(tipo, COLOR_PARED)

        # Fondo de la celda de la estacion
        pygame.draw.rect(superficie, color, rect, border_radius=8)
        pygame.draw.rect(superficie, COLOR_LINEA, rect, 2, border_radius=8)

        # Etiqueta centrada (tipo abreviado)
        cx = rect.centerx
        cy = rect.centery - 8
        _texto(superficie, est.etiqueta(), fuente, COLOR_TEXTO, cx, cy)

        # Nombre debajo de la etiqueta (mas pequeño)
        nombre_corto = est.nombre[:6] if len(est.nombre) > 6 else est.nombre
        _texto(superficie, nombre_corto, fuente, COLOR_TEXTO_TENUE, cx, cy + 18)


def dibujar_chefs(superficie, chefs, chef_activo_idx, fuente):
    """
    Dibuja los dos chefs en sus posiciones actuales.
    El chef activo tiene un borde blanco para destacarlo.

    superficie       : pantalla pygame
    chefs            : lista de objetos Chef (cocina.chefs)
    chef_activo_idx  : indice del chef activo (cocina._chef_activo)
    fuente           : fuente para mostrar el ingrediente que carga
    """
    for i, chef in enumerate(chefs):
        rect = _rect_celda(chef.fila, chef.columna)

        # Circulo del chef (usa el color definido en mapas.py)
        centro = rect.center
        radio = TAMANO_CELDA // 2 - 8
        pygame.draw.circle(superficie, chef.color, centro, radio)

        # Borde blanco si es el chef activo
        if i == chef_activo_idx:
            pygame.draw.circle(superficie, COLOR_TEXTO, centro, radio, 3)

        # Inicial del chef encima
        inicial = chef.nombre[-1]  # "1" o "2"
        _texto(superficie, inicial, fuente, COLOR_FONDO, centro[0], centro[1] - 6)

        # Si carga algo, mostrar las primeras letras del ingrediente debajo
        if chef.tiene_ingrediente():
            ing = chef.ingrediente
            etiqueta_ing = ing.nombre[:4].upper()
            _texto(superficie, etiqueta_ing, fuente, COLOR_TEXTO,
                   centro[0], centro[1] + 10)


def dibujar_hud(superficie, cocina, fuente_grande, fuente):
    """
    Dibuja la barra superior con tiempo restante y puntaje.

    superficie   : pantalla pygame
    cocina       : objeto Cocina (para leer tiempo y puntaje)
    fuente_grande: fuente mediana para tiempo y puntaje
    fuente       : fuente chica para etiquetas
    """
    # Fondo de la barra HUD
    barra = pygame.Rect(0, 0, ANCHO_TABLERO, Y_TABLERO + 2)
    pygame.draw.rect(superficie, COLOR_PARED, barra)

    # Tiempo restante (izquierda)
    minutos = int(cocina.tiempo) // 60
    segundos = int(cocina.tiempo) % 60
    tiempo_str = f"{minutos}:{segundos:02d}"
    _texto(superficie, f"TIEMPO  {tiempo_str}", fuente_grande,
           COLOR_TEXTO, 160, Y_TABLERO // 2 + 2)

    # Puntaje (centro-derecha)
    _texto(superficie, f"PUNTAJE  {cocina.puntaje}", fuente_grande,
           COLOR_OK, 500, Y_TABLERO // 2 + 2)

    # Mapa y dificultad (derecha)
    _texto(superficie, f"{cocina.nombre_mapa}  ·  {cocina.dificultad}",
           fuente, COLOR_TEXTO_TENUE, 760, Y_TABLERO // 2 + 2)


def dibujar_mensaje(superficie, mensaje, tiempo_restante_msg, fuente):
    """
    Muestra un mensaje de feedback en la parte baja del tablero
    (ej. 'Tomaste Pan', 'Entregaste Hamburguesa Clasica! +40 puntos').
    El mensaje se desvanece cuando tiempo_restante_msg llega a 0.

    superficie          : pantalla pygame
    mensaje             : string a mostrar
    tiempo_restante_msg : float, segundos que le quedan al mensaje
    fuente              : fuente para el texto
    """
    if not mensaje or tiempo_restante_msg <= 0:
        return

    # Fondo semitransparente en la parte baja del tablero
    alto_msg = 32
    fondo = pygame.Surface((ANCHO_TABLERO, alto_msg), pygame.SRCALPHA)
    alpha = min(255, int(255 * tiempo_restante_msg / 2.0))  # desvanece en 2s
    fondo.fill((0, 0, 0, alpha // 2))
    superficie.blit(fondo, (X_TABLERO, Y_TABLERO + ALTO_TABLERO - alto_msg))

    color_msg = (*COLOR_OK, alpha) if "+" in mensaje else (*COLOR_TEXTO, alpha)
    sup = fuente.render(mensaje, True, color_msg[:3])
    sup.set_alpha(alpha)
    cx = X_TABLERO + ANCHO_TABLERO // 2
    cy = Y_TABLERO + ALTO_TABLERO - alto_msg // 2
    rect = sup.get_rect(center=(cx, cy))
    superficie.blit(sup, rect)


def dibujar_controles(superficie, fuente):
    """
    Muestra los controles en la esquina inferior del panel lateral.
    Se llama desde main.py pasando la posicion correcta.
    """
    controles = [
        "WASD : mover",
        "E    : interactuar",
        "TAB  : cambiar chef",
        "1/2/3: mapa",
        "R    : reiniciar",
        "ESC  : salir",
    ]
    x = ANCHO_TABLERO + 20
    y = ALTO_VENTANA - len(controles) * 22 - 10
    for linea in controles:
        sup = fuente.render(linea, True, COLOR_TEXTO_TENUE)
        superficie.blit(sup, (x, y))
        y += 22