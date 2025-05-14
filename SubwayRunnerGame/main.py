import pygame
import random
import os

pygame.init()
pygame.mixer.init()


base_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(base_dir, "assets", "wallpaper.jpg")
sprite_sheet_path = os.path.join(base_dir, "assets", "64x64 sprite sheet.png")
heart_image_path = os.path.join(base_dir, "assets", "heart.png")
music_path = os.path.join(base_dir, "assets", "music.mp3")


monster_sprite_path = os.path.join(base_dir, "assets", "aliensprite.png")
obstacle_sprite_path = os.path.join(base_dir, "assets", "Sun.png")


pygame.mixer.music.load(music_path)
pygame.mixer.music.play(loops=-1, start=0.0)


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Subway Runner")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
LIGHT_PINK = (255, 105, 180)

background_image = pygame.image.load(background_path).convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite


heart_image = pygame.image.load(heart_image_path).convert_alpha()


monster_sprite = pygame.image.load(monster_sprite_path).convert_alpha()
monster_sprite = pygame.transform.scale(monster_sprite, (32, 32))

obstacle_sprite = pygame.image.load(obstacle_sprite_path).convert_alpha()
obstacle_sprite = pygame.transform.scale(obstacle_sprite, (64, 64))


frame_width = 64
frame_height = 64
frame_count = 6
frame_index = 0
frame_rate = 0.1
last_update_time = 0


x = 100
y = 300
speed = 5


start_time = pygame.time.get_ticks()
safe_duration = 2000


num_obstacles = 8
obstacle_width = 64
obstacle_height = 64
obstacles = []

def is_far_enough(new_rect, others, min_dist=200):
    for obs in others:
        if new_rect.colliderect(obs.inflate(min_dist, min_dist)):
            return False
    return True

attempts = 0
max_attempts = 1000

while len(obstacles) < num_obstacles and attempts < max_attempts:
    x_pos = random.randint(100, screen_width - 100 - obstacle_width)
    y_pos = random.randint(100, screen_height - 100 - obstacle_height)
    new_obstacle = pygame.Rect(x_pos, y_pos, obstacle_width, obstacle_height)
    if is_far_enough(new_obstacle, obstacles):
        obstacles.append(new_obstacle)
    attempts += 1


coins = []

def add_new_coin():
    max_attempts = 100
    for _ in range(max_attempts):
        new_coin = pygame.Rect(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30), 30, 30)
        too_close = False
        for obs in obstacles:
            if new_coin.colliderect(obs.inflate(60, 60)):
                too_close = True
                break
        if not too_close:
            coins.append(new_coin)
            break

for _ in range(20):
    add_new_coin()


monster_width = 32
monster_height = 32

monsters = [
    pygame.Rect(random.randint(0, screen_width - monster_width),
                random.randint(0, screen_height - monster_height),
                monster_width, monster_height)
]

score = 0
game_over = False
lives = 3
invincible = False
invincible_start_time = 0


score_multiplier = 1
multiplier_time = 0
multiplier_duration = 10000
last_multiplier_time = 0
multiplier_rect = None

def move_monsters():
    for monster in monsters:
        direction = random.choice(["left", "right", "up", "down"])
        if direction == "left" and monster.x > 0:
            monster.x -= 4
        elif direction == "right" and monster.x < screen_width - monster.width:
            monster.x += 4
        elif direction == "up" and monster.y > 0:
            monster.y -= 4
        elif direction == "down" and monster.y < screen_height - monster.height:
            monster.y += 4

def add_monster():
    new_monster = pygame.Rect(random.randint(0, screen_width - monster_width),
                              random.randint(0, screen_height - monster_height),
                              monster_width, monster_height)
    monsters.append(new_monster)

def display_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_lives():
    for i in range(lives):
        screen.blit(heart_image, (screen_width - 150 + i * 40, 10))

def add_score_multiplier():
    multiplier_width = 30
    multiplier_height = 30
    new_multiplier = pygame.Rect(random.randint(0, screen_width - multiplier_width),
                                 random.randint(0, screen_height - multiplier_height),
                                 multiplier_width, multiplier_height)
    return new_multiplier


def draw_multiplier_bar():
    if score_multiplier > 1:
        elapsed = current_time - multiplier_time
        remaining = max(0, multiplier_duration - elapsed)
        bar_width = 200
        bar_height = 20
        bar_x = (screen_width - bar_width) // 2
        bar_y = 50

        fill_width = int(bar_width * (remaining / multiplier_duration))
        pygame.draw.rect(screen, PINK, (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)

running = True
while running:
    current_time = pygame.time.get_ticks()

    if game_over:
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(game_over_text, (screen_width // 4, screen_height // 3))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    else:

        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= speed
        if keys[pygame.K_RIGHT] and x < screen_width - frame_width:
            x += speed
        if keys[pygame.K_UP] and y > 0:
            y -= speed
        if keys[pygame.K_DOWN] and y < screen_height - frame_height:
            y += speed

        if current_time - last_update_time >= frame_rate * 1000:
            frame_index = (frame_index + 1) % frame_count
            last_update_time = current_time

        sprite = get_sprite(sprite_sheet, frame_index * frame_width, 0, frame_width, frame_height)
        screen.blit(sprite, (x, y))

        if current_time - last_multiplier_time >= 30000:
            if multiplier_rect is None:
                multiplier_rect = add_score_multiplier()
                last_multiplier_time = current_time

        if multiplier_rect is not None:
            pygame.draw.rect(screen, LIGHT_PINK, multiplier_rect)
            if pygame.Rect(x, y, frame_width, frame_height).colliderect(multiplier_rect):
                score_multiplier = 2
                multiplier_time = current_time
                multiplier_rect = None
                add_monster()

        if score_multiplier > 1 and current_time - multiplier_time >= multiplier_duration:
            score_multiplier = 1

        for obstacle in obstacles:
            screen.blit(obstacle_sprite, (obstacle.x, obstacle.y))
            if current_time - start_time > safe_duration:
                if obstacle.colliderect(pygame.Rect(x, y, frame_width, frame_height)) and not invincible:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        invincible = True
                        invincible_start_time = current_time

        for coin in coins[:]:
            pygame.draw.circle(screen, (255, 223, 0), (coin.x + 15, coin.y + 15), 15)
            if pygame.Rect(x, y, frame_width, frame_height).colliderect(coin):
                coins.remove(coin)
                score += 1 * score_multiplier
                add_new_coin()

                if score % 10 == 0:
                    add_monster()

        for monster in monsters[:]:
            screen.blit(monster_sprite, (monster.x, monster.y))
            if current_time - start_time > safe_duration:
                if pygame.Rect(x, y, frame_width, frame_height).colliderect(monster) and not invincible:
                    lives -= 1
                    monsters.remove(monster)
                    if lives <= 0:
                        game_over = True
                    else:
                        invincible = True
                        invincible_start_time = current_time

        if invincible and current_time - invincible_start_time >= 5000:
            invincible = False

        move_monsters()
        display_score()
        display_lives()
        draw_multiplier_bar()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

pygame.quit()
