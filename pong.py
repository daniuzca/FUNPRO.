import pygame
import sys

# --- constants -------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED = 5

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- helper classes -------------------------------------------------------
class Paddle(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.top > 0:
            self.y -= self.speed

    def move_down(self):
        if self.bottom < HEIGHT:
            self.y += self.speed


class Ball(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED

    def reset(self, direction=1):
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.vx = BALL_SPEED * direction
        self.vy = BALL_SPEED if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED


# --- drawing --------------------------------------------------------------
def draw_screen(screen, paddles, ball, score1, score2, font):
    screen.fill(BLACK)
    for paddle in paddles:
        pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    # center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{score1}   {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()


# --- main ----------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # select mode
    mode = menu(screen, font, clock)

    left = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
    ball.reset(direction=1)

    score1 = 0
    score2 = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # movement
        keys = pygame.key.get_pressed()
        # left paddle (player 1)
        if keys[pygame.K_w]:
            left.move_up()
        if keys[pygame.K_s]:
            left.move_down()

        # right paddle
        if mode == "2P":
            if keys[pygame.K_UP]:
                right.move_up()
            if keys[pygame.K_DOWN]:
                right.move_down()
        else:  # AI
            ai_move(right, ball)

        # ball movement
        ball.x += ball.vx
        ball.y += ball.vy

        # collisions with top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball.vy *= -1

        # paddle collisions
        if ball.colliderect(left) and ball.vx < 0:
            ball.vx *= -1
        if ball.colliderect(right) and ball.vx > 0:
            ball.vx *= -1

        # score
        if ball.left <= 0:
            score2 += 1
            ball.reset(direction=1)
        if ball.right >= WIDTH:
            score1 += 1
            ball.reset(direction=-1)

        draw_screen(screen, (left, right), ball, score1, score2, font)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def ai_move(paddle, ball):
    # simple AI: follows the ball's y position
    if paddle.centery < ball.centery and paddle.bottom < HEIGHT:
        paddle.y += paddle.speed
    if paddle.centery > ball.centery and paddle.top > 0:
        paddle.y -= paddle.speed


def menu(screen, font, clock):
    # display a simple menu to choose 2-player or vs computer
    options = ["1. Two Player", "2. Vs Computer"]
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return "2P" if selected == 0 else "AI"

        screen.fill(BLACK)
        for i, opt in enumerate(options):
            color = WHITE if i == selected else (100, 100, 100)
            text = font.render(opt, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
