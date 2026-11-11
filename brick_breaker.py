import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - AI Coding Zone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GRAY = (100, 100, 100)

# Game variables
FPS = 60
clock = pygame.time.Clock()

# Paddle settings
paddle_width = 120
paddle_height = 20
paddle_speed = 8
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50

# Ball settings
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = -5

# Brick settings
brick_rows = 6
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30
brick_padding = 5

# Game state
score = 0
lives = 3
level = 1
game_state = "menu"  # menu, playing, paused, game_over, win

# Font
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)
font_tiny = pygame.font.Font(None, 24)

# Power-ups
powerups = []
powerup_types = ['expand', 'shrink', 'speed', 'slow', 'multiball', 'life']

class Brick:
    def __init__(self, x, y, color, hits=1):
        self.rect = pygame.Rect(x, y, brick_width - brick_padding, brick_height - brick_padding)
        self.color = color
        self.hits = hits
        self.max_hits = hits
        self.active = True
        
    def draw(self):
        if self.active:
            # Draw brick with gradient effect
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)
            
            # Draw hits indicator
            if self.max_hits > 1:
                hit_text = font_tiny.render(str(self.hits), True, WHITE)
                text_rect = hit_text.get_rect(center=self.rect.center)
                screen.blit(hit_text, text_rect)
                
    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.active = False
            return True
        return False

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = ball_radius
        self.active = True
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
    def draw(self):
        if self.active:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius - 3)

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.speed = 3
        self.radius = 15
        self.active = True
        self.colors = {
            'expand': GREEN,
            'shrink': RED,
            'speed': ORANGE,
            'slow': BLUE,
            'multiball': PURPLE,
            'life': PINK
        }
        
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.active = False
            
    def draw(self):
        if self.active:
            pygame.draw.circle(screen, self.colors[self.type], (int(self.x), int(self.y)), self.radius)
            # Draw symbol
            symbol = self.type[0].upper()
            text = font_tiny.render(symbol, True, WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(text, text_rect)

def create_bricks(level):
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    
    for row in range(brick_rows):
        for col in range(brick_cols):
            x = col * brick_width + brick_padding
            y = row * brick_height + brick_padding + 80
            color = colors[row % len(colors)]
            
            # Higher levels have stronger bricks
            hits = 1 if level == 1 else min(level, 3)
            if row == 0:  # Top row is always stronger
                hits = min(level + 1, 3)
                
            brick = Brick(x, y, color, hits)
            bricks.append(brick)
            
    return bricks

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    angle = random.uniform(-45, 45)
    speed = 7
    ball_speed_x = speed * (1 if random.random() > 0.5 else -1)
    ball_speed_y = -speed

def draw_menu():
    screen.fill(BLACK)
    
    # Title with glow effect
    title = font_large.render("BRICK BREAKER", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title, title_rect)
    
    # Menu options
    play_text = font_medium.render("Press SPACE to Play", True, GREEN)
    play_rect = play_text.get_rect(center=(WIDTH // 2, 300))
    screen.blit(play_text, play_rect)
    
    # Instructions
    instructions = [
        "Move Paddle: Arrow Keys or A/D",
        "Pause: P or ESC",
        "Collect Power-ups!",
        "",
        "Power-ups:",
        "G = Expand Paddle",
        "R = Shrink Paddle",
        "O = Speed Up Ball",
        "B = Slow Down Ball",
        "P = Multi-ball",
        "H = Extra Life"
    ]
    
    y_offset = 370
    for instruction in instructions:
        inst_text = font_tiny.render(instruction, True, GRAY if instruction == "" else WHITE)
        inst_rect = inst_text.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(inst_text, inst_rect)
        y_offset += 25
        
    # Credits
    credit = font_tiny.render("AI Coding Zone", True, BLUE)
    credit_rect = credit.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(credit, credit_rect)

def draw_game():
    screen.fill(BLACK)
    
    # Draw bricks
    for brick in bricks:
        brick.draw()
        
    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, BLUE, (paddle_x + 5, paddle_y + 5, paddle_width - 10, paddle_height - 10))
    
    # Draw balls
    for ball in balls:
        ball.draw()
        
    # Draw power-ups
    for powerup in powerups:
        powerup.draw()
        
    # Draw UI
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    lives_text = font_small.render(f"Lives: {lives}", True, RED)
    screen.blit(lives_text, (10, 45))
    
    level_text = font_small.render(f"Level: {level}", True, GREEN)
    level_rect = level_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(level_text, level_rect)

def draw_pause():
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pause_text = font_large.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(pause_text, pause_rect)
    
    resume_text = font_small.render("Press P or ESC to Resume", True, GREEN)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(resume_text, resume_rect)

def draw_game_over():
    screen.fill(BLACK)
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(game_over_text, game_over_rect)
    
    final_score = font_medium.render(f"Final Score: {score}", True, WHITE)
    score_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(final_score, score_rect)
    
    restart_text = font_small.render("Press SPACE to Restart", True, GREEN)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(restart_text, restart_rect)
    
    menu_text = font_tiny.render("Press ESC for Menu", True, GRAY)
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
    screen.blit(menu_text, menu_rect)

def draw_win():
    screen.fill(BLACK)
    
    # Draw fireworks effect
    for i in range(20):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK])
        pygame.draw.circle(screen, color, (x, y), random.randint(2, 5))
    
    win_text = font_large.render("LEVEL COMPLETE!", True, GREEN)
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(win_text, win_rect)
    
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    next_text = font_small.render("Press SPACE for Next Level", True, YELLOW)
    next_rect = next_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(next_text, next_rect)

def apply_powerup(type):
    global paddle_width, ball_speed_x, ball_speed_y, lives
    
    if type == 'expand':
        paddle_width = min(paddle_width + 30, 200)
    elif type == 'shrink':
        paddle_width = max(paddle_width - 30, 60)
    elif type == 'speed':
        ball_speed_x *= 1.3
        ball_speed_y *= 1.3
    elif type == 'slow':
        ball_speed_x *= 0.7
        ball_speed_y *= 0.7
    elif type == 'multiball':
        for i in range(2):
            angle = random.uniform(-45, 45)
            new_ball = Ball(balls[0].x, balls[0].y, 
                          ball_speed_x + random.uniform(-2, 2),
                          ball_speed_y + random.uniform(-2, 2))
            balls.append(new_ball)
    elif type == 'life':
        lives += 1

# Initialize game
bricks = create_bricks(level)
balls = [Ball(ball_x, ball_y, ball_speed_x, ball_speed_y)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_SPACE:
                    game_state = "playing"
                    score = 0
                    lives = 3
                    level = 1
                    paddle_width = 120
                    bricks = create_bricks(level)
                    balls = [Ball(ball_x, ball_y, ball_speed_x, ball_speed_y)]
                    powerups.clear()
                    
            elif game_state == "playing":
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    game_state = "paused"
                    
            elif game_state == "paused":
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    game_state = "playing"
                    
            elif game_state == "game_over":
                if event.key == pygame.K_SPACE:
                    game_state = "playing"
                    score = 0
                    lives = 3
                    level = 1
                    paddle_width = 120
                    bricks = create_bricks(level)
                    balls = [Ball(ball_x, ball_y, ball_speed_x, ball_speed_y)]
                    powerups.clear()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    
            elif game_state == "win":
                if event.key == pygame.K_SPACE:
                    level += 1
                    game_state = "playing"
                    paddle_width = max(120 - (level * 5), 80)
                    bricks = create_bricks(level)
                    balls = [Ball(ball_x, ball_y, ball_speed_x * 1.1, ball_speed_y * 1.1)]
                    powerups.clear()
    
    if game_state == "playing":
        # Paddle movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
            paddle_x -= paddle_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed
            
        # Ball movement and collision
        for ball in balls[:]:
            if not ball.active:
                continue
                
            ball.move()
            
            # Wall collision
            if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
                ball.speed_x *= -1
            if ball.y - ball.radius <= 0:
                ball.speed_y *= -1
                
            # Bottom collision (lose life)
            if ball.y + ball.radius >= HEIGHT:
                ball.active = False
                balls.remove(ball)
                if len(balls) == 0:
                    lives -= 1
                    if lives <= 0:
                        game_state = "game_over"
                    else:
                        balls = [Ball(ball_x, ball_y, ball_speed_x, ball_speed_y)]
                        
            # Paddle collision
            if (paddle_y <= ball.y + ball.radius <= paddle_y + paddle_height and
                paddle_x <= ball.x <= paddle_x + paddle_width):
                ball.speed_y = -abs(ball.speed_y)
                # Add angle based on where ball hits paddle
                hit_pos = (ball.x - paddle_x) / paddle_width
                ball.speed_x = (hit_pos - 0.5) * 10
                
            # Brick collision
            for brick in bricks:
                if not brick.active:
                    continue
                    
                if brick.rect.collidepoint(ball.x, ball.y):
                    # Determine collision side
                    if abs(ball.x - brick.rect.left) < ball.radius or abs(ball.x - brick.rect.right) < ball.radius:
                        ball.speed_x *= -1
                    else:
                        ball.speed_y *= -1
                        
                    if brick.hit():
                        score += 10 * level
                        
                        # Chance to spawn power-up
                        if random.random() < 0.2:  # 20% chance
                            powerup_type = random.choice(powerup_types)
                            powerup = PowerUp(brick.rect.centerx, brick.rect.centery, powerup_type)
                            powerups.append(powerup)
                    break
                    
        # Power-up movement and collection
        for powerup in powerups[:]:
            if not powerup.active:
                powerups.remove(powerup)
                continue
                
            powerup.move()
            
            # Check collision with paddle
            if (paddle_y <= powerup.y <= paddle_y + paddle_height and
                paddle_x <= powerup.x <= paddle_x + paddle_width):
                apply_powerup(powerup.type)
                powerup.active = False
                score += 5
                
        # Check win condition
        if all(not brick.active for brick in bricks):
            game_state = "win"
    
    # Drawing
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "paused":
        draw_game()
        draw_pause()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "win":
        draw_win()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()