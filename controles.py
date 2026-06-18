import pygame
from chef import ARRIBA, ABAJO, IZQUIERDA, DERECHA

# Teclas WASD para mover al chef activo.
TECLAS_DIRECCION = {
    pygame.K_w: ARRIBA,
    pygame.K_s: ABAJO,
    pygame.K_a: IZQUIERDA,
    pygame.K_d: DERECHA,
}


def direccion_desde_teclas(teclas_presionadas):
    for tecla, direccion in TECLAS_DIRECCION.items():
        if teclas_presionadas[tecla]:
            return direccion
    return None