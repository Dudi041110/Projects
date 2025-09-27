import pygame
import sys
import random
import os

pygame.init()
pygame.display.set_caption("Day and Night")
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()

fps_font = pygame.font.SysFont(None, 30)
font_path = os.path.join(os.path.dirname(__file__), "Assets", "PixelatedPusab.ttf")
font = pygame.font.Font(font_path, 48)

full_heart = pygame.transform.scale((pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "full heart.png")).convert_alpha()), (75, 75))
half_heart = pygame.transform.scale((pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "half heart.png")).convert_alpha()), (75, 75))
empty_heart = pygame.transform.scale((pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "empty heart.png")).convert_alpha()), (75, 75))

health = 6

GraveStone = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "GraveStone.png")).convert_alpha()
GraveStone_height, GraveStone_width = GraveStone.get_height(), GraveStone.get_width()
GraveStone = pygame.transform.scale(GraveStone, (GraveStone_width // 1.75, GraveStone_height // 1.75))

sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "gosth.png")).convert_alpha()

ghost_sprites = []
ghost_x, ghost_y = 500, 730
for i in range(4):
    x = i * 25
    frame = sheet.subsurface(pygame.Rect(x, 0, 25, 25))
    ghost_sprites.append(pygame.transform.scale(frame, (200, 200)))

room = 3

points = 0

room_ground = {
    1: [pygame.Rect(0, 750, 1920, 330), pygame.Rect(0, 0, 20, 1080)],
    2: [pygame.Rect(0, 750, 1920, 330), pygame.Rect(650, 500, 1270, 580), pygame.Rect(350, 625, 300, 455)],
    3: [pygame.Rect(0, 500, 300, 580), pygame.Rect(0, 700, 550, 380), pygame.Rect(0, 900, 1920, 180), pygame.Rect(1500, 750, 420, 330)]
}

player_x, player_y, player_side_length, player_border_side_length, player_y_velocity = 200,  50, 100, 120, 0

Attack_timer = 0
attack = pygame.Rect(0, 0, 0, 0)
delayed_attack = pygame.Rect(0, 0, 0, 0)

def player_movement():
    global player_x, player_y, player_y_velocity, repeat
    
    player_hurtbox = pygame.Rect(player_x - 10, player_y - 10, player_border_side_length, player_border_side_length )
    player_ground_hitbox = pygame.Rect(player_x + 15, player_y, player_border_side_length - 30, player_border_side_length,)
    player_right_side_hitbox = pygame.Rect(player_x + player_side_length, player_y + 10, 10, player_side_length - 20)
    player_left_side_hitbox = pygame.Rect(player_x - 10, player_y + 10, 10, player_side_length - 20)

    on_ground = False
    for ground in room_ground[room]:
        if player_ground_hitbox.colliderect(ground):
            on_ground = True
            break
    
    right_side_touching = False
    for ground in room_ground[room]:
        if player_right_side_hitbox.colliderect(ground):
            right_side_touching = True
            break

    left_side_touching = False
    for ground in room_ground[room]:
        if player_left_side_hitbox.colliderect(ground):
            left_side_touching = True
            break

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not left_side_touching:
        player_x -= 3
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not right_side_touching:
        player_x += 3
    if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and repeat < 4:
        player_y_velocity = 5
        repeat += 0.1
    elif on_ground:
        repeat = 0
    else:
        repeat = 5
    
    player_y -= player_y_velocity
    if on_ground:
        player_y_velocity = 0
    else:
        player_y_velocity -= 0.1

def decorations():
    if room == 3:
        screen.blit(GraveStone, (825, 660))    

def ghost_ai():
    global ghost_hurtbox, ghost_x, ghost_y, ghost_direction
    ghost_hurtbox = pygame.Rect(ghost_x + 32, ghost_y + 32, 120, 136)


def fighting():
    global Attack_timer, attack, left_fist, right_fist, top_fist, delayed_attack

    left_fist = pygame.Rect(player_x - 60, player_y + 25, 50, 50)
    right_fist = pygame.Rect(player_x + 110, player_y + 25, 50, 50)
    top_fist = pygame.Rect(player_x + 25, player_y - 60, 50, 50)

    keys = pygame.key.get_pressed()

    # Only start a new attack if no attack is active
    if Attack_timer <= 0:
        if keys[pygame.K_j]:
            attack = left_fist
            delayed_attack = left_fist
            Attack_timer = 20
        elif keys[pygame.K_l]:
            attack = right_fist
            delayed_attack = right_fist
            Attack_timer = 20
        elif keys[pygame.K_k]:
            attack = top_fist
            delayed_attack = top_fist
            Attack_timer = 20

    # Countdown timer
    if Attack_timer > 0:
        Attack_timer -= 1
    else:
        attack = pygame.Rect(0, 0, 0, 0)  # Clear attack
        delayed_attack = None

    return attack

    

def room_change():
    global room, player_x, player_y
    if player_x + 50 >= 1920:
        room += 1
        player_x = 0
    if player_x + 50 <= 0:
        room -= 1
        player_x = 1820

def sky():
    global room, day
    if room in (1, 2):
        day = True
        screen.fill((208, 246, 255))
        pygame.draw.circle(screen, (255, 243, 128), (50, 50), 150)
    else:
        day = False
        screen.fill((28,28,56))
        pygame.draw.circle(screen, (84, 84, 84), (1870, 50), 150)
        pygame.draw.circle(screen, (107, 107, 107), (1820, 50), 50)
        pygame.draw.circle(screen, (107, 107, 107), (1875, 130), 30)
        pygame.draw.circle(screen, (107, 107, 107), (1810, 130), 20)

def health_bar():
    global health

    if health == 6:
        screen.blit(full_heart, (10, 60))
        screen.blit(full_heart, (80, 60))
        screen.blit(full_heart, (150, 60))
    elif health == 5:
        screen.blit(full_heart, (10, 60))
        screen.blit(full_heart, (80, 60))
        screen.blit(half_heart, (150, 60))
    elif health == 4:
        screen.blit(full_heart, (10, 60))
        screen.blit(full_heart, (80, 60))
        screen.blit(empty_heart, (150, 60))
    elif health == 3:
        screen.blit(full_heart, (10, 60))
        screen.blit(half_heart, (80, 60))
        screen.blit(empty_heart, (150, 60))
    elif health == 2:
        screen.blit(full_heart, (10, 60))
        screen.blit(empty_heart, (80, 60))
        screen.blit(empty_heart, (150, 60))
    elif health == 1:
        screen.blit(half_heart, (10, 60))
        screen.blit(empty_heart, (80, 60))
        screen.blit(empty_heart, (150, 60))

def fps_counter():
    fps = int(clock.get_fps())
    if day:
        fps_text = fps_font.render(f"FPS: {fps}", True, (0, 0, 0))
    else:
        fps_text = fps_font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (1800, 10))

def draw():
    sky()
    decorations()
    pygame.draw.rect(screen, (173, 116, 17), (player_x - 10, player_y - 10, player_border_side_length, player_border_side_length), border_radius = 20)
    pygame.draw.rect(screen, (255, 171, 25), (player_x - 2.5, player_y - 2.5, player_side_length + 5, player_side_length + 5), border_radius = 20)
    pygame.draw.rect(screen, (255, 213, 102), fighting(), border_radius = 20)
    for ground in room_ground[room]:
        pygame.draw.rect(screen, (0, 204, 68), ground,)
    if day:
        screen.blit(font.render(f"Points: {points}", True, (0, 0, 0)), (10, 10))
    else:
        screen.blit(font.render(f"Points: {points}", True, (255, 255, 255)), (10, 10))
    health_bar()
    ghost_ai()
    fps_counter()
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player_movement()
    room_change()
    draw()
    clock.tick(175)

pygame.quit()
sys.exit()