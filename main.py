import pygame
import random
import sys

def __rocks__(screen, rocks, screen_width, screen_height, rock_img, rock_speed_range):
    rock_width, rock_height = rock_img.get_size()

    # спавн
    if random.random() < 0.05:  # 5% шанс за кадр
        x_pos = random.randint(0, screen_width - rock_width)
        y_pos = -rock_height
        speed = random.choice(rock_speed_range)
        rocks.append([x_pos, y_pos, speed])

    # рух
    for rock in rocks:
        rock[1] += rock[2]

    # чистка
    rocks[:] = [rock for rock in rocks if rock[1] < screen_height]

    # малювання
    for rock in rocks:
        screen.blit(rock_img, (rock[0], rock[1]))


def __player__(keys, player_pos, player_speed, event=None):
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

def check_collision(player_pos, player_img, rocks, rock_img, screen):
    player_rect = pygame.Rect(
        player_pos[0] + 5,
        player_pos[1] + 5,
        player_img.get_width() - 10,
        player_img.get_height() - 10
    )

    for rock in rocks:
        rock_rect = pygame.Rect(
            rock[0] + 8,
            rock[1] + 8,
            rock_img.get_width() - 16,
            rock_img.get_height() - 16
        )

        # pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)
        # pygame.draw.rect(screen, (0, 255, 0), rock_rect, 2)

        if player_rect.colliderect(rock_rect):
            return True  # зіткнення є

    return False  # все ок

def __main__(event=None):
    pygame.init() # ініціалізуємо pygame
    screen = pygame.display.set_mode((1200, 800)) # створюємо вікно
    clock = pygame.time.Clock()  # для контролю FPS

    # створюємо гравця
    player_img = pygame.image.load("player.png")  # завантажуємо зображення
    player_pos = [500, 400]  # координати
    player_speed = 5  # швидкість руху
    player_img = pygame.transform.scale(player_img, (50, 76.6))  # 100 пікселів ширина, 150 висота

    # створюємо камені
    rocks = []
    screen_width, screen_height = 1200, 800

    rock_img = pygame.image.load("rock.png")  # камінь-зображення
    rock_img = pygame.transform.scale(rock_img, (50, 50))  # задаємо розмір
    rock_speed_range = [4,6] # задаємо швидкфсть каменя

    # для виходу з програми
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        __player__(keys, player_pos, player_speed)  # оновлюємо координати

        screen.fill((0, 0, 0)) # очищаєм екран

        # малюємо елементи гри
        screen.blit(player_img, player_pos)  # малюємо на екрані
        __rocks__(screen, rocks, screen_width, screen_height, rock_img, rock_speed_range)

        if check_collision(player_pos, player_img, rocks, rock_img, screen):
            print("GAME OVER")
            pygame.time.delay(1500)
            pygame.quit()
            sys.exit()

        pygame.display.flip()  # оновлюємо екран
        clock.tick(60)  # 60 FPS

if __name__ == '__main__':
    __main__()