import pygame,random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("shooter")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 2
        self.speed_x=0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-5,5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


#BackGround de fondo
background = pygame.image.load("assets/background.png").convert()
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()


player = Player()
all_sprites.add(player)

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# Pantalla de inicio
font = pygame.font.Font(None, 36)
start_text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(start_text, start_text_rect)
pygame.display.flip()

waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            waiting_for_start = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False


running = True
paused = False  # Variable para controlar la pausa
collision_count = 0  # Contador de colisiones
max_collisions = 3  # Máximo de colisiones permitidas
meteoritos_eliminados = 0


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_p:  # Pausar y reanudar con la tecla "p"
                paused = not paused
            elif event.key == pygame.K_q:  # Salir del juego en pausa con la tecla "q"
                if paused:
                    pygame.quit()
                    running = False


    if not paused:  # Solo actualiza el juego si no está en pausa
        all_sprites.update()


    #validar colisiones - laser - meteoro
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        meteoritos_eliminados += len(hits)

    #validar colisiones - jugador - meteoro

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    if hits:
        collision_count += 1
        if collision_count >= max_collisions:
            # Pantalla de Game Over
            font = pygame.font.Font(None, 25)
            game_over_text = font.render("¡Game Over! Presiona ESPACIO para continuar.", True, WHITE)
            game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, game_over_text_rect)
            pygame.display.flip()

            # Restablecer contador de colisiones
            collision_count = 0

            # Limpiar todos los meteoritos actuales
            for meteor in meteor_list:
                meteor.kill()

            # Generar nuevos meteoritos
            for i in range(8):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteor_list.add(meteor)

            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        waiting_for_restart = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting_for_restart = False

    screen.blit(background,[0,0])
    # Mostrar el contador de meteoritos eliminados en la esquina superior derecha
    font = pygame.font.Font(None, 36)
    contador_text = font.render(f"Meteoritos eliminados: {meteoritos_eliminados}", True, WHITE)
    contador_text_rect = contador_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(contador_text, contador_text_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()



