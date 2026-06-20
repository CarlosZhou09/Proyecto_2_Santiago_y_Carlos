import pygame
COLOR_FONDO       = (28, 30, 38)
COLOR_PARED       = (38, 40, 52)
COLOR_PISO        = (52, 56, 70)
COLOR_TEXTO       = (235, 235, 245)
COLOR_TEXTO_TENUE = (160, 165, 180)
COLOR_OK          = (110, 210, 130)
COLOR_FREIDORA    = (200, 160, 70)
COLOR_ALERTA      = (235, 110, 110)
 

# Pequeño ayudante: barra de tiempo de UNA receta
def _dibujar_barra_tiempo(superficie, receta, x, y, ancho, alto=8):
    """Dibuja la barra de tiempo restante de una receta (verde -> amarillo -> rojo)."""
    frac = max(0.0, min(1.0, receta.tiempo_restante / receta.tiempo_maximo))
    fondo = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(superficie, COLOR_FONDO, fondo, border_radius=4)
    relleno = pygame.Rect(x, y, int(ancho * frac), alto)
    if frac > 0.4:
        color = COLOR_OK
    elif frac > 0.15:
        color = COLOR_FREIDORA      # amarillo/naranja de advertencia
    else:
        color = COLOR_ALERTA
    pygame.draw.rect(superficie, color, relleno, border_radius=4)
 
# Panel lateral de ordenes activas
def dibujar_panel_ordenes(superficie, ordenes, x, y, ancho, alto,
                          fuente_titulo, fuente):
    """
    Dibuja el panel lateral derecho con las ordenes activas.
    superficie    : pantalla de pygame donde dibujar.
    ordenes       : lista de Receta activas (gestor.ordenes).
    x, y          : esquina superior izquierda del panel.
    ancho, alto   : tamaño del panel.
    fuente_titulo : fuente para el titulo "ORDENES".
    fuente        : fuente chica para el contenido de cada tarjeta.
    """
    panel = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(superficie, COLOR_PARED, panel)
 
    titulo = fuente_titulo.render("ORDENES", True, COLOR_TEXTO)
    superficie.blit(titulo, (x + 14, y + 10))
 
    cy = y + 40
    for receta in ordenes:
        tarjeta = pygame.Rect(x + 10, cy, ancho - 20, 66)
        pygame.draw.rect(superficie, COLOR_PISO, tarjeta, border_radius=6)
 
        # Nombre de la receta
        nombre = fuente.render(receta.nombre, True, COLOR_TEXTO)
        superficie.blit(nombre, (tarjeta.x + 8, tarjeta.y + 6))
 
        # Puntos actuales (a la derecha)
        pts = fuente.render(f"{receta.puntos_actuales} pts", True, COLOR_OK)
        superficie.blit(pts, (tarjeta.right - pts.get_width() - 8, tarjeta.y + 6))
 
        # Ingredientes requeridos (resumen)
        resumen = fuente.render(receta.resumen(), True, COLOR_TEXTO_TENUE)
        superficie.blit(resumen, (tarjeta.x + 8, tarjeta.y + 26))
 
        # Barra de tiempo de esta receta
        _dibujar_barra_tiempo(superficie, receta,
                              tarjeta.x + 8, tarjeta.bottom - 14, tarjeta.width - 16)
        cy += 74
 
        if cy > y + alto - 66:   # no dibujar fuera del panel
            break
 
 
# Pantalla de fin de juego
def dibujar_fin_juego(superficie, puntaje, ancho, alto,
                      fuente_grande, fuente, fuente_chica,
                      instruccion="R: reiniciar     ESC: salir"):
    """
    Dibuja un velo oscuro encima de todo + "TIEMPO!" + el puntaje final.
    superficie     : pantalla de pygame (del tamaño total de la ventana).
    puntaje        : puntaje final a mostrar (gestor.puntaje).
    ancho, alto    : tamaño total de la ventana.
    fuente_grande  : fuente grande para el titulo.
    fuente         : fuente mediana para el puntaje.
    fuente_pequena   : fuente pequeña para la instruccion.
    """
    velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    velo.fill((0, 0, 0, 180))
    superficie.blit(velo, (0, 0))
 
    def centrado(texto, fuente_x, color, cy):
        sup = fuente_x.render(texto, True, color)
        rect = sup.get_rect(center=(ancho // 2, cy))
        superficie.blit(sup, rect)
 
    centrado("TIEMPO!", fuente_grande, COLOR_TEXTO, alto // 2 - 40)
    centrado(f"Puntaje final: {puntaje}", fuente, COLOR_OK, alto // 2)
    centrado(instruccion, fuente_chica, COLOR_TEXTO_TENUE, alto // 2 + 36)
 