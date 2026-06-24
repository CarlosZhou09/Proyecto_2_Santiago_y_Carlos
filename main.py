"""
main.py
-------
Bucle principal de Crazy Snack Rush TEC.

Es el unico archivo que toca pygame directamente (aparte de Interfaz.py
de Santiago e interfaz_juego.py). Su unica responsabilidad es:
  1. Inicializar pygame y crear la ventana.
  2. Leer el teclado y traducirlo a acciones de Cocina.
  3. Llamar a Cocina.actualizar(dt) cada frame.
  4. Llamar a las funciones de dibujo en el orden correcto.
  5. Cerrar pygame al salir.

Controles:
  WASD      : mover chef activo
  E         : interactuar con estacion al frente
  TAB       : cambiar de chef
  1 / 2 / 3 : cargar mapa Burger Bytes / Taco Logic / Gourmet Stack
  R         : reiniciar el mapa actual
  ESC       : salir
"""

import pygame
import sys

from cocina import Cocina
from mapas import ORDEN_MAPAS
from controles import direccion_desde_teclas

# Funciones de dibujo propias (tablero, chefs, HUD, mensajes)
import interfaz_juego as ij

# Funciones de dibujo de Santiago (panel ordenes, fin de juego)
from Interfaz import dibujar_panel_ordenes, dibujar_fin_juego

# -----------------------------------------------------------------------
# Constantes de la ventana
# -----------------------------------------------------------------------
ANCHO  = 1280
ALTO   = 720
FPS    = 60
TITULO = "Crazy Snack Rush TEC"

# Duracion del mensaje de feedback en pantalla (segundos)
DURACION_MENSAJE = 2.5


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()

    # Fuentes
    fuente_grande = pygame.font.SysFont("consolas", 20, bold=True)
    fuente        = pygame.font.SysFont("consolas", 14)
    fuente_chica  = pygame.font.SysFont("consolas", 12)
    fuente_fin    = pygame.font.SysFont("consolas", 48, bold=True)

    # Estado inicial
    clave_mapa_actual = ORDEN_MAPAS[0]   # empieza en Burger Bytes
    cocina = Cocina(clave_mapa_actual)

    # Mensaje de feedback (lo que devuelve interactuar_chef_activo)
    mensaje         = ""
    tiempo_mensaje  = 0.0

    # Tecla E: registrar si ya se proceso en este frame para no repetir
    e_presionada_antes = False

    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000.0   # segundos desde el frame anterior

        # -----------------------------------------------------------
        # 1. EVENTOS (cierre de ventana, teclas de un solo disparo)
        # -----------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:

                # Salir
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                # Cambiar de chef (TAB)
                elif evento.key == pygame.K_TAB:
                    cocina.cambiar_chef()

                # Interactuar (E) - un solo disparo al presionar
                elif evento.key == pygame.K_e:
                    if not cocina.terminado():
                        msg = cocina.interactuar_chef_activo()
                        if msg:
                            mensaje = msg
                            tiempo_mensaje = DURACION_MENSAJE

                # Cargar mapa 1 / 2 / 3
                elif evento.key == pygame.K_1:
                    clave_mapa_actual = ORDEN_MAPAS[0]
                    cocina = Cocina(clave_mapa_actual)
                    mensaje, tiempo_mensaje = "", 0.0

                elif evento.key == pygame.K_2:
                    clave_mapa_actual = ORDEN_MAPAS[1]
                    cocina = Cocina(clave_mapa_actual)
                    mensaje, tiempo_mensaje = "", 0.0

                elif evento.key == pygame.K_3:
                    clave_mapa_actual = ORDEN_MAPAS[2]
                    cocina = Cocina(clave_mapa_actual)
                    mensaje, tiempo_mensaje = "", 0.0

                # Reiniciar mapa actual (R)
                elif evento.key == pygame.K_r:
                    cocina = Cocina(clave_mapa_actual)
                    mensaje, tiempo_mensaje = "", 0.0

        # -----------------------------------------------------------
        # 2. MOVIMIENTO CONTINUO (WASD, se lee cada frame)
        # -----------------------------------------------------------
        if not cocina.terminado():
            teclas = pygame.key.get_pressed()
            direccion = direccion_desde_teclas(teclas)
            if direccion:
                cocina.mover_chef_activo(direccion)

        # -----------------------------------------------------------
        # 3. ACTUALIZAR LOGICA
        # -----------------------------------------------------------
        cocina.actualizar(dt)

        if tiempo_mensaje > 0:
            tiempo_mensaje -= dt

        # -----------------------------------------------------------
        # 4. DIBUJAR
        # -----------------------------------------------------------
        # 4a. Fondo general
        ij.dibujar_fondo(pantalla)

        # 4b. Tablero cuadriculado
        ij.dibujar_tablero(pantalla)

        # 4c. Estaciones
        ij.dibujar_estaciones(pantalla, cocina.estaciones, fuente)

        # 4d. Chefs
        ij.dibujar_chefs(pantalla, cocina.chefs, cocina._chef_activo, fuente)

        # 4e. HUD (tiempo + puntaje + nombre del mapa)
        ij.dibujar_hud(pantalla, cocina, fuente_grande, fuente_chica)

        # 4f. Mensaje de feedback
        ij.dibujar_mensaje(pantalla, mensaje, tiempo_mensaje, fuente)

        # 4g. Panel lateral de ordenes (Santiago)
        dibujar_panel_ordenes(
            pantalla,
            cocina.ordenes,
            x=ij.ANCHO_TABLERO,
            y=0,
            ancho=ANCHO - ij.ANCHO_TABLERO,
            alto=ALTO - 160,
            fuente_titulo=fuente_grande,
            fuente=fuente
        )

        # 4h. Controles en la esquina del panel lateral
        ij.dibujar_controles(pantalla, fuente_chica)

        # 4i. Pantalla de fin de juego encima de todo (si termino)
        if cocina.terminado():
            dibujar_fin_juego(
                pantalla,
                cocina.puntaje,
                ANCHO,
                ALTO,
                fuente_fin,
                fuente_grande,
                fuente_chica
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()