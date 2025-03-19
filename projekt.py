import pygame
import random

pygame.init()

# Skärmstorlek
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Chase")

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Spelvariabler
player_size = enemy_size = food_size = boost_size = 30
player_speed = 5
boost_speed = 10
enemy_speed = 3

# Skapa spelobjekt
player = pygame.Rect(WIDTH//2, HEIGHT//2, player_size, player_size)
enemy = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), enemy_size, enemy_size)
food = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), food_size, food_size)
boost = None

running = True
score = 0
clock = pygame.time.Clock()
current_speed = player_speed
boost_active = False

while running:
    screen.fill(BLACK)
    
    # Visa poängen
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Spelarens rörelser
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= current_speed
    if keys[pygame.K_RIGHT]: player.x += current_speed
    if keys[pygame.K_UP]: player.y -= current_speed
    if keys[pygame.K_DOWN]: player.y += current_speed
    
    # Begränsa spelaren inom skärmen
    player.clamp_ip(screen.get_rect())
    
    # Fienden rör sig mot spelaren
    enemy.x += enemy_speed if player.x > enemy.x else -enemy_speed
    enemy.y += enemy_speed if player.y > enemy.y else -enemy_speed
    
    # Kollision med mat
    if player.colliderect(food):
        food.x, food.y = random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30)
        score += 1
        if score % 10 == 0 and not boost:
            boost = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), boost_size, boost_size)
    
    # Kollision med boost
    if boost and player.colliderect(boost):
        boost = None
        current_speed = boost_speed
        boost_active = True
        pygame.time.set_timer(pygame.USEREVENT, 3000)
    
    # Kollision med fiende
    if player.colliderect(enemy):
        print(f"Game Over! Your score: {score}")
        running = False
    
    # Rita objekt
    pygame.draw.rect(screen, YELLOW if not boost_active else BLUE, player)
    pygame.draw.rect(screen, RED, enemy)
    pygame.draw.rect(screen, WHITE, food)
    if boost: pygame.draw.rect(screen, BLUE, boost)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
