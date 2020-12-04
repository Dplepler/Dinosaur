import pygame
import sys
import random


def drop_enemies(score, counter, speed, line_y, screen, red, player_size, drop_enemy_x, drop_enemy_y, random_number, width):
    """
    the function makes random enemies drop from the sky when the score hits 100
    """
    drop_enemy_y_check = False
    is_falling = False
    drop_enemy_size = player_size
    if score > 100:
        if not is_falling:
            if counter == random_number:
                is_falling = True
                if is_falling:
                    drop_enemy_y += speed
                    if not drop_enemy_y_check:
                        if drop_enemy_y == line_y + speed:
                            drop_enemy_y_check = True
                            if drop_enemy_y_check:
                                drop_enemy_x -= speed
                                drop_enemy_y -= speed
                                if drop_enemy_x == 0:
                                    is_falling = False
                                    drop_enemy_y = 0
                                    drop_enemy_x = width // 2
                                    random_number = random.randint(3, 10)
                                    counter = 0
                    pygame.draw.rect(screen, red, (drop_enemy_x, drop_enemy_y, drop_enemy_size, drop_enemy_size))
    pygame.display.update()
    print(drop_enemy_x)
    return drop_enemy_y, drop_enemy_x, random_number, counter


def pause(screen, white, pink, height, width, clock):
    paused = True
    paused_text = "Paused"
    paused_text_2 = "Press SPACE to continue"
    font = pygame.font.SysFont("comicsans ms", 80)
    font_2 = pygame.font.SysFont("comicsansms", 40)
    while paused:
        screen.fill(white)
        pause_label = font.render(paused_text, 1, pink)
        pause_label2 = font_2.render(paused_text_2, 1, pink)
        screen.blit(pause_label, (width // 3, height // 3))
        screen.blit(pause_label2, (width // 4, height // 3 + 80))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
        pygame.display.update()
        clock.tick(5)


def draw(x, y, screen, enemy_x, enemy_y, enemy_size_x, player_size):
    pewdiepie = pygame.image.load("pewdiepie.png")
    screen.blit(pewdiepie, (x, y))
    sheep = pygame.image.load("sheep.png")
    sheep_extent = pygame.image.load("sheep_extent_1.png")
    if enemy_size_x == 50:
        screen.blit(sheep, (enemy_x, enemy_y))
    if enemy_size_x == 100:
        screen.blit(sheep, (enemy_x, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size, enemy_y))
    if enemy_size_x == 150:
        screen.blit(sheep, (enemy_x, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size * 2, enemy_y))
    if enemy_size_x == 200:
        screen.blit(sheep, (enemy_x, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size * 2, enemy_y))
        screen.blit(sheep_extent, (enemy_x + player_size * 3, enemy_y))


def collisions(enemy_x, x, enemy_y, y, enemy_size_x, player_size, enemy_size_y, drop_enemy_x, drop_enemy_y):
    if (x <= enemy_x <= x + player_size and y <= enemy_y <= y + player_size) or (enemy_y + enemy_size_y >= y + player_size >= enemy_y and enemy_x + enemy_size_x >= x >= enemy_x):
        game_over = True
        return game_over
    elif (x <= drop_enemy_x <= x + player_size and y <= drop_enemy_y <= y + player_size) or (drop_enemy_y + player_size >= y + player_size >= drop_enemy_y and drop_enemy_x + player_size >= x >= drop_enemy_x):
        game_over = True
        return game_over


def move_enemies(enemy_x, speed):
    enemy_x -= speed
    return enemy_x


def jumping(jump_pressed, y, velocity):
    if jump_pressed:
        y -= velocity
        velocity -= 1
    if velocity == 0:
        jump_pressed = False

    return y, jump_pressed, velocity


def returning(y, jump_pressed, line_y, velocity):
    if y < line_y and not jump_pressed:
        velocity += 1
        y += velocity
    return y, velocity


def main():
    pygame.init()
    width = 800
    height = 600
    background = [105, 105, 105]
    white = [255, 255, 255]
    red = [255, 51, 0]
    black = [0, 0, 0]
    screen = pygame.display.set_mode((width, height))
    screen.fill(background)
    game_over = False
    clock = pygame.time.Clock()
    FPS = 100
    speed = 10
    player_size = 50
    x = 100
    y = 400
    line_y = height - 200
    enemy_size_x_list = [50, 100, 150, 200]
    velocity = 20
    enemy_x = width - player_size
    enemy_y = line_y
    enemy_size_x = random.choice(enemy_size_x_list)
    enemy_size_y = player_size
    jump_pressed = False
    counter = 0
    drop_enemy_x = width // 2
    drop_enemy_y = 0
    random_number = random.randint(3, 10)
    score = 0
    text = "Score: " + str(score)
    myfont = pygame.font.SysFont("monospace", 35)
    while not game_over:
        label = myfont.render(text, 1, white)
        screen.blit(label, (width // 2, height // 2))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and y == line_y:
                    if jump_pressed is not True:
                        jump_pressed = True
                elif event.key == pygame.K_p:
                    pause(screen, white, red, height, width, clock)
        y, jump_pressed, velocity = jumping(jump_pressed, y, velocity)
        y, velocity = returning(y, jump_pressed, line_y, velocity)
        screen.fill(background)
        pygame.draw.rect(screen, white, (x, y, player_size, player_size))
        pygame.draw.rect(screen, background, (enemy_x, enemy_y, enemy_size_x, enemy_size_y))
        pygame.draw.line(screen, black, (0, line_y + player_size), (width, line_y + player_size))
        draw(x, y, screen, enemy_x, enemy_y, enemy_size_x, enemy_size_y)
        enemy_x = move_enemies(enemy_x, speed)
        # summon enemies
        if enemy_x < x - player_size * 5:
            enemy_size_x = random.choice(enemy_size_x_list)
            enemy_x = width
            enemy_y = line_y
            pygame.draw.rect(screen, red, (enemy_x, enemy_y, enemy_size_x, enemy_size_y))
            score += 100
            counter += 1
        drop_enemy_y, drop_enemy_x, random_number, counter = drop_enemies(score, counter, speed, line_y, screen, red, player_size, drop_enemy_x, drop_enemy_y, random_number, width)
        game_over = collisions(enemy_x, x, enemy_y, y, enemy_size_x, player_size, enemy_size_y, drop_enemy_x, drop_enemy_y)
        text = "Score: " + str(score)
        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()
