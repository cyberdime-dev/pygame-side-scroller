import pygame
import sys
from player import Player
from platform import Platform
from settings import *

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroller")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 36)

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
game_state = STATE_MENU

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

# Load background
bg = pygame.image.load("assets/bg.png").convert()
scroll = 0

# Setup player and platforms
player = Player(100, HEIGHT - 150)
platforms = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle(player)

for i in range(5):
    platform = Platform(i * 200, HEIGHT - 50)
    platforms.add(platform)

# --- Button Rendering ---
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = BUTTON_HOVER if x < mouse[0] < x + w and y < mouse[1] < y + h else BUTTON_COLOR
    pygame.draw.rect(SCREEN, color, (x, y, w, h), border_radius=10)
    label = FONT.render(text, True, WHITE)
    SCREEN.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    if x < mouse[0] < x + w and y < mouse[1] < y + h and click[0] and action:
        pygame.time.delay(200)
        action()

# --- State Handlers ---
def start_game():
    global game_state, player, player_group
    player.rect.topleft = (100, HEIGHT - 150)
    player.vel_y = 0
    game_state = STATE_PLAYING

def quit_game():
    pygame.quit()
    sys.exit()

def restart_game():
    global game_state
    game_state = STATE_MENU

def draw_menu():
    SCREEN.fill(BLACK)
    title = FONT.render("Side Scroller", True, WHITE)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    draw_button("Start", 300, 250, 200, 60, start_game)
    draw_button("Quit", 300, 350, 200, 60, quit_game)

def draw_game():
    global scroll

    scroll -= 2
    if scroll <= -WIDTH:
        scroll = 0
    SCREEN.blit(bg, (scroll, 0))
    SCREEN.blit(bg, (scroll + WIDTH, 0))

    keys = pygame.key.get_pressed()
    player.update(keys)
    player_group.draw(SCREEN)
    platforms.draw(SCREEN)

    # Platform collision
    for platform in platforms:
        if player.rect.colliderect(platform.rect) and player.vel_y > 0:
            player.rect.bottom = platform.rect.top
            player.vel_y = 0
            player.jumping = False

    if player.rect.top > HEIGHT:
        return STATE_GAME_OVER

    return STATE_PLAYING

def draw_game_over():
    SCREEN.fill(BLACK)
    msg = FONT.render("Game Over!", True, WHITE)
    SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 100))
    draw_button("Restart", 300, 250, 200, 60, restart_game)
    draw_button("Quit", 300, 350, 200, 60, quit_game)

def draw_win():
    SCREEN.fill(BLACK)
    msg = FONT.render("You Win!", True, WHITE)
    SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 100))
    draw_button("Restart", 300, 250, 200, 60, restart_game)
    draw_button("Quit", 300, 350, 200, 60, quit_game)

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYING:
        game_state = draw_game()
    elif game_state == STATE_GAME_OVER:
        draw_game_over()
    elif game_state == STATE_WIN:
        draw_win()

    pygame.display.update()
    CLOCK.tick(FPS)
