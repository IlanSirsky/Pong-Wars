import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Color palette
colorPalette = {
    'ArcticPowder': "#F1F6F4",
    'MysticMint': "#D9E8E3",
    'Forsythia': "#FFC801",
    'DeepSaffron': "#FF9932",
    'NocturnalExpedition': "#114C5A",
    'OceanicNoir': "#172B36",
}

# Constants
DAY_COLOR = colorPalette['MysticMint']
DAY_BALL_COLOR = colorPalette['NocturnalExpedition']
NIGHT_COLOR = colorPalette['NocturnalExpedition']
NIGHT_BALL_COLOR = colorPalette['MysticMint']
SQUARE_SIZE = 25
WIDTH, HEIGHT = 800, 800  # Canvas size

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day and Night Pong")
clock = pygame.time.Clock()

# Initialize squares
numSquaresX = WIDTH // SQUARE_SIZE
numSquaresY = HEIGHT // SQUARE_SIZE
squares = [[DAY_COLOR if i < numSquaresX // 2 else NIGHT_COLOR for j in range(numSquaresY)] for i in range(numSquaresX)]

# Ball setup
x1, y1 = WIDTH // 4, HEIGHT // 2
dx1, dy1 = 14, 14
x2, y2 = (WIDTH // 4) * 3, HEIGHT // 2
dx2, dy2 = -14, -14


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def draw_ball(x, y, color):
    pygame.draw.circle(screen, hex_to_rgb(color), (int(x), int(y)), SQUARE_SIZE // 2)


def draw_squares():
    for i in range(numSquaresX):
        for j in range(numSquaresY):
            pygame.draw.rect(screen, hex_to_rgb(squares[i][j]),
                             (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def random_num(min, max):
    return random.uniform(min, max)


def update_square_and_bounce(x, y, dx, dy, color):
    updated_dx, updated_dy = dx, dy

    for angle in range(0, 360, 45):
        rad_angle = math.radians(angle)
        check_x = x + math.cos(rad_angle) * (SQUARE_SIZE // 2)
        check_y = y + math.sin(rad_angle) * (SQUARE_SIZE // 2)

        i, j = int(check_x // SQUARE_SIZE), int(check_y // SQUARE_SIZE)

        if 0 <= i < numSquaresX and 0 <= j < numSquaresY:
            if squares[i][j] != color:
                squares[i][j] = color

                if abs(math.cos(rad_angle)) > abs(math.sin(rad_angle)):
                    updated_dx = -updated_dx
                else:
                    updated_dy = -updated_dy

                updated_dx += random_num(-0.01, 0.01)
                updated_dy += random_num(-0.01, 0.01)

    return updated_dx, updated_dy


def check_boundary_collision(x, y, dx, dy):
    if x + dx > WIDTH - SQUARE_SIZE // 2 or x + dx < SQUARE_SIZE // 2:
        dx = -dx
    if y + dy > HEIGHT - SQUARE_SIZE // 2 or y + dy < SQUARE_SIZE // 2:
        dy = -dy

    return dx, dy


def count_squares():
    day_count = sum(squares[i][j] == DAY_COLOR for i in range(numSquaresX) for j in range(numSquaresY))
    night_count = sum(squares[i][j] == NIGHT_COLOR for i in range(numSquaresX) for j in range(numSquaresY))
    return day_count, night_count

# Set up font for rendering text
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(hex_to_rgb(colorPalette['ArcticPowder']))
    draw_squares()

    draw_ball(x1, y1, DAY_BALL_COLOR)
    dx1, dy1 = update_square_and_bounce(x1, y1, dx1, dy1, DAY_COLOR)

    draw_ball(x2, y2, NIGHT_BALL_COLOR)
    dx2, dy2 = update_square_and_bounce(x2, y2, dx2, dy2, NIGHT_COLOR)

    dx1, dy1 = check_boundary_collision(x1, y1, dx1, dy1)
    dx2, dy2 = check_boundary_collision(x2, y2, dx2, dy2)

    x1 += dx1
    y1 += dy1
    x2 += dx2
    y2 += dy2

    # Count and display the squares
    day_count, night_count = count_squares()
    score_text = font.render(f"Day: {day_count} | Night: {night_count}", True, (0, 0, 0))  # Black color

    # Get the width and height of the text surface
    text_width, text_height = score_text.get_size()

    # Calculate position for the text: bottom center
    text_x = (WIDTH - text_width) // 2
    text_y = HEIGHT - text_height - 10  # 10 pixels above the bottom

    screen.blit(score_text, (text_x, text_y))  # Position the text

    pygame.display.flip()
    clock.tick(150)

pygame.quit()
