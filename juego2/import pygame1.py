import pygame
import random

# Inicialización del juego
pygame.init()

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Creación de la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego")

# Cargar imagenes
player_img = pygame.image.load("descarga.png")
enemy_img = pygame.image.load("descargat.png")

# Cambiar el tamaño de las imágenes
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.vel_y = 0
        self.jump = False

    def update(self):
        # Gravedad
        self.vel_y += 0.5
        if self.vel_y > 8:
            self.vel_y = 8

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = -10
            self.jump = True

        # Aplicar gravedad
        self.rect.y += self.vel_y
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.jump = False

# Clase de enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, WIDTH - self.rect.width)
        self.rect.y = random.randint(100, HEIGHT - self.rect.height)
        self.vel_x = random.choice([-2, 2])
        self.vel_y = random.choice([-2, 2])

    def update(self):
        # Movimiento del enemigo
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Cambio de dirección al colisionar con los límites de la ventana
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel_x = -self.vel_x
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -self.vel_y

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Creación del jugador
player = Player()
all_sprites.add(player)

# Creación de enemigos
for i in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Puntaje
score = 0

# Ciclo principal del juego
running = True
clock = pygame.time.Clock()
while running:
    # Frecuencia de actualización del juego
    clock.tick(60)

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualización de los sprites
    all_sprites.update()

    # Colisiones del jugador con los enemigos
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False  # Termina el juego si el jugador colisiona con un enemigo

    # Renderizado del juego
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    # Mostrar puntaje en la pantalla
    font = pygame.font.Font(None, 36)
    score_text = font.render("Puntaje: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# Finalización del juego
pygame.quit()
