import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🥚 Egg Drop - Arcade Edition")

# Colors
SKY_BLUE = (135, 206, 250)
GRADIENT_TOP = (173, 216, 230)
GRADIENT_BOTTOM = (135, 206, 250)
WHITE = (255, 255, 255)
WOOD_BROWN = (160, 82, 45)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
DARK_GRAY = (40, 40, 40)
HOVER_COLOR = (70, 70, 70)
TEXT_COLOR = (255, 255, 255)

# Game variables
FPS = 60
EGG_RADIUS = 20
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
EGG_FALL_SPEED = 6
BASKET_SPEED = 10
MAX_MISSES = 3

# Fonts
font = pygame.font.SysFont("Verdana", 36)
small_font = pygame.font.SysFont("Verdana", 28)

# Basket
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, HEIGHT - 60, BASKET_WIDTH, BASKET_HEIGHT)

# Game state
score = 0
misses = 0
eggs = []
paused = False
game_over_flag = False

clock = pygame.time.Clock()

# ----------------- BUTTON FUNCTIONALITY ------------------

def draw_gradient_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = GRADIENT_TOP[0] * (1 - ratio) + GRADIENT_BOTTOM[0] * ratio
        g = GRADIENT_TOP[1] * (1 - ratio) + GRADIENT_BOTTOM[1] * ratio
        b = GRADIENT_TOP[2] * (1 - ratio) + GRADIENT_BOTTOM[2] * ratio
        pygame.draw.line(WIN, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = HOVER_COLOR if hovered else DARK_GRAY

    pygame.draw.rect(WIN, color, (x, y, w, h), border_radius=10)
    text_surf = small_font.render(text, True, TEXT_COLOR)
    WIN.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))

    if click[0] == 1 and hovered:
        pygame.time.delay(200)
        if action:
            action()

def restart_game():
    global score, misses, eggs, paused, game_over_flag
    score = 0
    misses = 0
    eggs.clear()
    paused = False
    game_over_flag = False
    basket.x = WIDTH // 2 - BASKET_WIDTH // 2

def end_game():
    pygame.quit()
    sys.exit()

def toggle_pause():
    global paused
    paused = not paused

# ----------------- DRAW FUNCTION ------------------

def draw_window():
    draw_gradient_background()

    # Draw basket
    pygame.draw.rect(WIN, WOOD_BROWN, basket, border_radius=10)

    # Draw eggs
    for egg in eggs:
        egg_color = random.choice([(255, 105, 180), (255, 215, 0), (173, 255, 47)])

        # Create an ellipse to simulate egg shape
        egg_rect = pygame.Rect(egg.x - EGG_RADIUS, egg.y - EGG_RADIUS, EGG_RADIUS * 1.2, EGG_RADIUS * 1.6)
        pygame.draw.ellipse(WIN, egg_color, egg_rect)

        # Add glossy shine
        highlight_rect = pygame.Rect(egg.x - EGG_RADIUS // 2, egg.y - EGG_RADIUS // 2, EGG_RADIUS // 2, EGG_RADIUS // 2)
        pygame.draw.ellipse(WIN, (255, 255, 255), highlight_rect)


    # Score and misses
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    miss_text = font.render(f"Misses: {misses}", True, RED)
    WIN.blit(score_text, (20, 20))
    WIN.blit(miss_text, (20, 70))

    # Buttons
    draw_button("Pause" if not paused else "Resume", 420, 20, 150, 40, toggle_pause)
    draw_button("Restart", 420, 70, 150, 40, restart_game)
    draw_button("Quit", 420, 120, 150, 40, end_game)

    pygame.display.update()

# ----------------- GAME OVER SCREEN ------------------

def game_over_screen():
    over_text = font.render("Game Over!", True, RED)
    WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.update()

# ----------------- GAME LOOP ------------------

def spawn_egg():
    x = random.randint(EGG_RADIUS, WIDTH - EGG_RADIUS)
    egg = pygame.Rect(x, 0, EGG_RADIUS * 2, EGG_RADIUS * 2)
    eggs.append(egg)

def main():
    global score, misses, paused, game_over_flag
    egg_timer = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

        if not paused and not game_over_flag:
            egg_timer += 1
            if egg_timer >= 60:
                spawn_egg()
                egg_timer = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and basket.x - BASKET_SPEED > 0:
                basket.x -= BASKET_SPEED
            if keys[pygame.K_RIGHT] and basket.x + BASKET_SPEED < WIDTH - BASKET_WIDTH:
                basket.x += BASKET_SPEED

            for egg in eggs[:]:
                egg.y += EGG_FALL_SPEED
                if egg.colliderect(basket):
                    eggs.remove(egg)
                    score += 1
                elif egg.y > HEIGHT:
                    eggs.remove(egg)
                    misses += 1

            if misses >= MAX_MISSES:
                game_over_flag = True

        draw_window()

        if game_over_flag:
            game_over_screen()

if __name__ == "__main__":
    main()
