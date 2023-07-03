import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana del juego
screen_width = 800
screen_height = 600

# Colores (en formato RGB)
black = (0, 0, 0)
white = (255, 255, 255)

# Creación de la ventana del juego
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Esquivar los obstáculos")

clock = pygame.time.Clock()

# Cargar efectos de sonido
pygame.mixer.music.load("ringtones-super-mario-bros.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

collision_sound = pygame.mixer.Sound("000215225_prev.mp3")
powerup_sound = pygame.mixer.Sound("080335_bonus-power-up-38379.mp3")

# Cargar imágenes
player_image = pygame.image.load("descarga.png")
obstacle_image = pygame.image.load("descargat.png")
powerup_image = pygame.image.load("descargac.png")
score_image = pygame.image.load("a.png")

# Escalar imágenes
player_image = pygame.transform.scale(player_image, (50, 50))
obstacle_image = pygame.transform.scale(obstacle_image, (random.randint(50, 100), 20))
powerup_image = pygame.transform.scale(powerup_image, (30, 30))
score_image = pygame.transform.scale(score_image, (150, 50))

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

# Clase de los obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-300, -20)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-300, -20)
            self.speed_y = random.randrange(1, 5)

# Clase del objeto de puntuación
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = score_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, 50)
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def update(self):
        self.text = self.font.render("Puntuación: {}".format(self.score), True, white)
        self.text_rect = self.text.get_rect(center=self.rect.center)

# Clase del power-up
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = powerup_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-300, -20)
        self.speed_y = random.randrange(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-300, -20)
            self.speed_y = random.randrange(1, 3)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Creación del jugador
player = Player()
all_sprites.add(player)

# Creación del objeto de puntuación
score = Score()
all_sprites.add(score)

# Creación de los obstáculos
for i in range(10):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Creación de power-ups
for i in range(5):
    powerup = Powerup()
    all_sprites.add(powerup)
    powerups.add(powerup)

# Nivel del juego
level = 1
level_font = pygame.font.Font(None, 24)
level_text = level_font.render("Nivel: {}".format(level), True, white)
level_rect = level_text.get_rect()
level_rect.topleft = (10, 10)

# Loop principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualización de los sprites
    all_sprites.update()

    # Colisiones entre el jugador y los obstáculos
    if pygame.sprite.spritecollide(player, obstacles, True):
        collision_sound.play()
        running = False

    # Colisiones entre el jugador y los power-ups
    powerup_collisions = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_collisions:
        powerup_sound.play()
        score.score += 10

    # Incremento de la puntuación cuando se esquiva un obstáculo
    if player.rect.top <= 0:
        player.rect.top = screen_height - 50
        score.score += 1

    # Pasar al siguiente nivel si la puntuación alcanza cierto umbral
    if score.score >= level * 10:
        level += 1
        level_text = level_font.render("Nivel: {}".format(level), True, white)
        level_rect = level_text.get_rect()
        level_rect.topleft = (10, 10)
        for i in range(level * 2):
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # Añadir power-ups adicionales en niveles pares
        if level % 2 == 0:
            for i in range(level // 2):
                powerup = Powerup()
                all_sprites.add(powerup)
                powerups.add(powerup)

    # Renderizado de la pantalla
    screen.fill(black)
    all_sprites.draw(screen)
    screen.blit(level_text, level_rect)
    pygame.display.flip()

    # Control de los FPS
    clock.tick(60)

# Mostrar la puntuación final
final_score_text = score.font.render("Puntuación final: {}".format(score.score), True, white)
final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(final_score_text, final_score_rect)
pygame.display.flip()

# Esperar unos segundos antes de cerrar la ventana
pygame.time.wait(3000)

# Finalización de Pygame
pygame.quit()
