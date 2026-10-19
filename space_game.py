import pygame
import sys
import random

# Αρχικοποίηση του Pygame
pygame.init()

# Ρυθμίσεις Οθόνης
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Cyberpunk Space Invaders"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Χρώματα (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Ρυθμίσεις Χρόνου (FPS)
clock = pygame.time.Clock()
FPS = 60

# --- ΔΗΜΙΟΥΡΓΙΑ CUSTOM SPRITES ΜΕ ΚΩΔΙΚΑ ---

# 1. Δημιουργία Διαστημοπλοίου (Player Sprite)
player_width = 50
player_height = 40
player_sprite = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
# Σχεδιάζουμε ένα τριγωνικό/κυβικό σκάφος με κυανό (cyan) χρώμα
pygame.draw.polygon(player_sprite, CYAN, [(25, 0), (0, 40), (10, 30), (40, 30), (50, 40)])
# Προσθέτουμε δύο μικρούς προωθητήρες (κίτρινους) στο πίσω μέρος
pygame.draw.rect(player_sprite, YELLOW, [12, 30, 6, 5])
pygame.draw.rect(player_sprite, YELLOW, [32, 30, 6, 5])

# 2. Δημιουργία Εξωγήινου (Enemy Sprite)
enemy_width = 45
enemy_height = 40
enemy_sprite = pygame.Surface((enemy_width, enemy_height), pygame.SRCALPHA)
# Σχεδιάζουμε το σώμα του εξωγήινου (κόκκινο οβάλ/κύβο)
pygame.draw.rect(enemy_sprite, RED, [5, 10, 35, 20], border_radius=5)
# Κέρατα / Κεραίες
pygame.draw.polygon(enemy_sprite, RED, [(10, 10), (5, 0), (15, 10)])
pygame.draw.polygon(enemy_sprite, RED, [(35, 10), (40, 0), (30, 10)])
# Μάτια (Λευκά με μαύρη κόρη)
pygame.draw.circle(enemy_sprite, WHITE, [15, 20], 4)
pygame.draw.circle(enemy_sprite, WHITE, [30, 20], 4)
pygame.draw.circle(enemy_sprite, BLACK, [15, 20], 1)
pygame.draw.circle(enemy_sprite, BLACK, [30, 20], 1)

# -------------------------------------------

# Αρχικές Θέσεις
player_x = (SCREEN_WIDTH // 2) - (player_width // 2)
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 7

enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 5

# Ρυθμίσεις Λέιζερ
bullet_width = 4
bullet_height = 15
bullet_speed = 12
bullets = []

# Σύστημα Σκορ
score = 0
font = pygame.font.SysFont("Arial", 36)

# Βασικό Game Loop
running = True
while running:
    
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                b_x = player_x + (player_width // 2) - (bullet_width // 2)
                b_y = player_y
                new_bullet = pygame.Rect(b_x, b_y, bullet_width, bullet_height)
                bullets.append(new_bullet)

    # 2. Update Game State
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if player_x < 0:
        player_x = 0
    if player_x > SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width

    # Κίνηση Εχθρού
    enemy_y += enemy_speed
    if enemy_y > SCREEN_HEIGHT:
        enemy_y = -enemy_height
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)

    # Κίνηση Λέιζερ
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Νοητά Rects για τις συγκρούσεις (χρησιμοποιούν τις διαστάσεις των νέων sprites)
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

    # Σύγκρουση: Εχθρός με Παίκτη
    if player_rect.colliderect(enemy_rect):
        print(f"GAME OVER! Τελικό Σκορ: {score}")
        running = False

    # Σύγκρουση: Λέιζερ με Εχθρό
    for bullet in bullets[:]:
        if bullet.colliderect(enemy_rect):
            bullets.remove(bullet)
            enemy_y = -enemy_height
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            score += 1
            # ΔΥΣΚΟΛΙΑ: Κάθε 3 level, ο εχθρός γίνεται ελαφρώς πιο γρήγορος!
            if score % 3 == 0:
                enemy_speed += 1

    # 3. Drawing (Σχεδίαση)
    screen.fill(BLACK)

    # Σχεδιάζουμε το custom διαστημόπλοιο αντί για το λευκό κουτί
    screen.blit(player_sprite, (player_x, player_y))

    # Σχεδιάζουμε τον custom εξωγήινο αντί για το κόκκινο κουτί
    screen.blit(enemy_sprite, (enemy_x, enemy_y))

    # Σχεδίαση όλων των λέιζερ (Cyberpunk στυλ)
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    # Σχεδίαση του Σκορ
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()