import pygame
import random


class Bullet:
    def __init__(self, x, y, profile):
        self.x = x+45
        self.y = y
        self.profile = profile
        self.speed = 5

    def move(self):
        self.y -= self.speed

    def is_out_of_screen(self):
        return self.y < 0


class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("alien.png"), (50, 50))

    def move(self):
        self.y += 0.05


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Set the title of the screen
pygame.display.set_caption('Galactic Space Shooter')

# Load images
background = pygame.image.load('background.jpg')
spaceship = pygame.image.load('spaceship.png')
bullet_prof = pygame.image.load('bullet.png')
font = pygame.font.Font(None, 36)

# Resize the images
spaceship = pygame.transform.scale(spaceship, (90, 80))
bullet_prof = pygame.transform.scale(bullet_prof, (20, 40))

# Set up the player
player_x = 370
player_y = 500
player_speed = 0.2

# Set up the alien
aliens = [Alien(random.randint(0, 700), random.randint(0, 100))]

# Set up the bullet
bullets = []
score = 0

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Draw the player's spaceship
    screen.blit(spaceship, (player_x, player_y))

    # Draw the alien
    for alien in aliens:
        screen.blit(alien.image, (alien.x, alien.y))

    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player_x, player_y, bullet_prof))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Keep player on the screen
    if player_x < 0:
        player_x = 750
    if player_x > 750:
        player_x = 0
    if player_y < 0:
        player_y = 0
    if player_y > 550:
        player_y = 550

    # Move the alien down the screen
    for alien in aliens:
        alien.move()
        if alien.y > 550:
            alien.y = random.randint(0, 100)
            alien.x = random.randint(0, 700)

    for bullet in bullets:
        screen.blit(bullet_prof, (bullet.x, bullet.y))
        # bullet.draw(screen)
        bullet.move()
        if bullet.is_out_of_screen():
            bullets.remove(bullet)
        for alien in aliens:
            distance_x = abs(bullet.x - alien.x)
            distance_y = abs(bullet.y - alien.y)
            if distance_x < 20 and distance_y < 20:
                score += 1
                alien.x = random.randint(0, 700)
                alien.y = random.randint(0, 100)
                bullets.remove(bullet)
                if score>0 and score%5 == 0: aliens.append(Alien(random.randint(0, 700), random.randint(0, 100)))

    for alien in aliens:
        distance_x = abs(player_x - alien.x)
        distance_y = abs(player_y - alien.y)
        if distance_x < 50 and distance_y < 50:
            running = False
    pygame.display.flip()


