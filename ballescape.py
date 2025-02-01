import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Escape")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius - 10
ball_speed = 5

# Line properties
line_width = 10
initial_line_y = HEIGHT // 2
line_speed = 2
hole_width = 100
buffer_zone = 5  # Buffer zone to avoid instant game over

# Score
score = 0
font = pygame.font.Font(None, 36)

# Generate initial line
def create_new_line():
    y_position = initial_line_y
    hole_x_start = random.randint(0, WIDTH - hole_width)
    return (y_position, hole_x_start, hole_width)

# Initialize the list with the first line
lines = [create_new_line()]

# Game loop variables
running = True
ball_dx = 0

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball_dx = -ball_speed
            elif event.key == pygame.K_RIGHT:
                ball_dx = ball_speed
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                ball_dx = 0

    # Update ball position
    ball_x += ball_dx
    ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))

    # Prepare batch drawing
    rects = []

    # Update line positions and check for game over
    for i, line in enumerate(lines):
        y, hole_x_start, hole_width = line
        y -= line_speed
        lines[i] = (y, hole_x_start, hole_width)

        # Check if the ball falls through the hole
        if y < ball_y < y + line_width - buffer_zone and not (hole_x_start <= ball_x <= hole_x_start + hole_width):
            running = False

        # Batch rect drawing for optimization
        rects.append(pygame.Rect(0, y, hole_x_start, line_width))
        rects.append(pygame.Rect(hole_x_start + hole_width, y, WIDTH - hole_x_start - hole_width, line_width))

    # Draw all lines in a single batch
    pygame.draw.rects(screen, BLACK, rects)

    # Remove off-screen lines and add new ones
    if lines[0][0] + line_width < 0:
        lines.pop(0)
        lines.append(create_new_line())
        score += 1
        line_speed += 0.1  # Increase speed gradually

    # Draw ball
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
