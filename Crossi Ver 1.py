import pygame
import sys
pygame.init()

# Pantalla
v_ancho  = 800
v_alto   = 800
v_titulo = "Crossi 1.0"
v_fps    = 30
# Colores
blanco   = (255, 255, 255)
negro    = (0, 0, 0)
gris     = (200, 200, 200)
# Reloj
reloj    = pygame.time.Clock() # Clock
# Fuente
comic_sans = pygame.font.SysFont("Comic Sans MS", 75) # Font

class VentanaJuego:
    # Constructor. Condiguracion de ventana
    def __init__(self, t, w, h, f):
        # Definicion de variables de clase (self)
        self.titulo = t
        self.ancho  = w
        self.alto   = h
        self.fps    = f
        # Configuracion de ventana
        self.ventana = pygame.display.set_mode((self.ancho, self.alto)) # Surface
        self.ventana.fill(blanco)
        pygame.display.set_caption(self.titulo)

    def ejecutar(self):
        game_over = False
        did_win   = False
        direccion = 0

        jugador     = PersonajeJugador("resource/player.png", 375, 700, 50, 50)
        enemigo0    = PersonajeEnemigo("resource/enemy.png", 20, 400, 50, 50)
        enemigo1    = PersonajeEnemigo("resource/enemy.png", 500, 300, 50, 50)
        tesoro      = ObjetoJuego("resource/treasure.png",375, 50, 50, 50)
        fondo       = ObjetoJuego("resource/background.png",0,0,self.ancho,self.alto)

        # Main Loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direccion = 1
                    elif event.key == pygame.K_DOWN:
                        direccion = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direccion = 0
                # print(event)

            self.ventana.fill(blanco)
            fondo.renderizar(self.ventana)
            tesoro.renderizar(self.ventana)
            enemigo0.mover(self.ancho)
            enemigo0.renderizar(self.ventana)
            enemigo1.mover(self.ancho)
            enemigo1.renderizar(self.ventana)
            jugador.mover(direccion, self.alto)
            jugador.renderizar(self.ventana)

            if jugador.colisiona(enemigo0) or jugador.colisiona(enemigo1):
                game_over = True
                did_win   = False
                texto = comic_sans.render("Perdiste", True, negro)
                self.ventana.blit(texto, ((self.ancho / 2)-(texto.get_width() / 2), (self.alto / 2)-(texto.get_height() / 2)))
                pygame.display.update()
                reloj.tick(1)
                break

            elif jugador.colisiona(tesoro):
                game_over = True
                did_win   = True
                texto = comic_sans.render("Ganaste", True, negro)
                self.ventana.blit(texto, ((self.ancho / 2)-(texto.get_width() / 2), (self.alto / 2)-(texto.get_height() / 2)))
                pygame.display.update()
                reloj.tick(1)
                break

            pygame.display.update()
            reloj.tick(self.fps)

        if did_win:
            self.ejecutar()

class ObjetoJuego:

    def __init__(self, source, x, y, w, h):
        # Cargar imagen
        source_load    = pygame.image.load(source)
        # Cambiar tamaño imagen
        self.image     = pygame.transform.scale(source_load, (w, h))
        # Posicion
        self.x_pos     = x
        self.y_pos     = y
        self.ancho_obj = w
        self.alto_obj  = h

    def renderizar(self, srfce):
        srfce.blit(self.image, (self.x_pos, self.y_pos))

class PersonajeJugador(ObjetoJuego):
    velocidad = 10

    # def __init__(self, source, x, y, w, h):
    #     super().__init__(source, x, y, w, h)

    def mover(self, direc, alto_ventana):
        # Si direc es positivo, se mueve para arriba
        if direc > 0:
            self.y_pos -= self.velocidad
        elif direc < 0:
            self.y_pos += self.velocidad

        # Si el jugador se pasa de la pantalla
        if self.y_pos < 0:
            self.y_pos = 0
        elif self.y_pos > alto_ventana - self.alto_obj:
            self.y_pos = alto_ventana - self.alto_obj

    def colisiona(self, otro_objeto):
        if self.y_pos >= otro_objeto.y_pos + otro_objeto.alto_obj:
            return False
        elif self.y_pos + self.alto_obj <= otro_objeto.y_pos:
            return False
        if otro_objeto.x_pos >= self.x_pos + self.ancho_obj:
            return False
        elif otro_objeto.x_pos + otro_objeto.ancho_obj <= self.x_pos:
            return False
        return True
            

class PersonajeEnemigo(ObjetoJuego):
    velocidad = 10

    # def __init__(self, source, x, y, w, h):
    #     super().__init__(source, x, y, w, h)

    def mover(self, ancho_ventana):
        # Si el enemigo sale de la pantalla
        if self.x_pos <= 0:
            self.velocidad = abs(self.velocidad)
        elif self.x_pos >= ancho_ventana - self.ancho_obj:
            self.velocidad = -abs(self.velocidad)

        self.x_pos += self.velocidad

nuevo_juego = VentanaJuego(v_titulo, v_ancho, v_alto, v_fps)

nuevo_juego.ejecutar()

pygame.quit()
sys.exit()