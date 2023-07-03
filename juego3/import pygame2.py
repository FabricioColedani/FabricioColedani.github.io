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

# Cargar imágenes
player_img = pygame.image.load("descarga.png")
enemy_img = pygame.image.load("descargat.png")
coin_img = pygame.image.load("descargac.png")

# Cambiar el tamaño de las imágenes
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
coin_img = pygame.transform.scale(coin_img, (30, 30))

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

# Clase de objetos a recolectar
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, WIDTH - self.rect.width)
        self.rect.y = random.randint(100, HEIGHT - self.rect.height)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Creación del jugador
player = Player()
all_sprites.add(player)

# Creación de enemigos
for i in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Creación de objetos a recolectar
for i in range(10):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Puntaje
score = 0

# Nivel
level = 1

# Fuente de texto
font = pygame.font.Font(None, 36)

# Pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Mi Juego", True, WHITE)
    instruction_text = font.render("Presiona ESPACIO para jugar", True, WHITE)
    screen.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - 50))
    screen.blit(instruction_text, (WIDTH/2 - instruction_text.get_width()/2, HEIGHT/2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Pantalla de fin de juego
def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render("Puntaje: " + str(score), True, WHITE)
    instruction_text = font.render("Presiona ESPACIO para jugar de nuevo", True, WHITE)
    screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - 50))
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2))
    screen.blit(instruction_text, (WIDTH/2 - instruction_text.get_width()/2, HEIGHT/2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Ciclo principal del juego
running = True
clock = pygame.time.Clock()
show_start_screen()
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

    # Colisiones del jugador con los objetos a recolectar
    coin_hits = pygame.sprite.spritecollide(player, coins, True)
    for coin in coin_hits:
        score += 10

    # Avanzar al siguiente nivel si se recolectaron todos los objetos
    if len(coins) == 0:
        level += 1
        for i in range(level * 2):
            coin = Coin()
            all_sprites.add(coin)
            coins.add(coin)

    # Renderizado del juego
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Mostrar puntaje y nivel en la pantalla
    score_text = font.render("Puntaje: " + str(score), True, BLACK)
    level_text = font.render("Nivel: " + str(level), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    pygame.display.flip()

# Pantalla de fin de juego
show_game_over_screen()

# Finalización del juego
pygame.quit()
