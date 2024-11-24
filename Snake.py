import pygame
import random
import time

# Pygame alustukset
pygame.init()

# Pelin värit
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Näytön asetukset
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Pelin kello
clock = pygame.time.Clock()

# Madon asetukset
block_size = 20
snake_speed = 15

# Fontit
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Pelin muuttujat
snake_pos = [[100, 50]]  # Lista, jossa maton ensimmäinen pala (x, y)
food_pos = [random.randrange(1, (screen_width // block_size)) * block_size,
            random.randrange(1, (screen_height // block_size)) * block_size]
food_spawn = True

direction = 'RIGHT'
change_to = direction
score = 0

# Aika, joka menee ennen pelin loppumista, kun mato syö ruoan
last_food_time = 0
food_timeout = 10  # 10 sekuntia

# Funktio pistemäärän näyttämiseen
def show_score(choice, color, font, size):
    value = score_font.render("Pisteet: " + str(score), True, color)
    screen.blit(value, [0, 0])

# Funktio, joka näyttää pelin päättymisviestin ja tarjoaa mahdollisuuden aloittaa peli uudelleen
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Peli ohi', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times new roman', 35)
    
    # Uudelleenpeluu- ja lopetuskutsu
    restart_font = pygame.font.SysFont('times new roman', 30)
    restart_surface = restart_font.render('Paina C aloittaaksesi uudelleen tai Q lopettaaksesi', True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (screen_width / 2, screen_height / 2 + 50)
    screen.blit(restart_surface, restart_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    main_game()  # Uudelleen käynnistä peli

# Pelin pääsilmukka
def main_game():
    global snake_pos, food_pos, food_spawn, direction, change_to, score, last_food_time

    snake_pos = [[100, 50]]
    food_pos = [random.randrange(1, (screen_width // block_size)) * block_size,
                random.randrange(1, (screen_height // block_size)) * block_size]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    last_food_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Varmista, ettei mato mene suoraan päinvastaiseen suuntaan
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Liikuta matoa
        if direction == 'UP':
            snake_pos[0][1] -= block_size
        if direction == 'DOWN':
            snake_pos[0][1] += block_size
        if direction == 'LEFT':
            snake_pos[0][0] -= block_size
        if direction == 'RIGHT':
            snake_pos[0][0] += block_size

        # Mato kasvaa
        snake_pos.insert(0, list(snake_pos[0]))  # Lisää uusi pala matoon

        # Tarkista, osuuko mato ruokaan
        if abs(snake_pos[0][0] - food_pos[0]) < block_size and abs(snake_pos[0][1] - food_pos[1]) < block_size:
            score += 10
            food_spawn = False  # Ruoka ei ole enää näkyvissä
            last_food_time = time.time()  # Tallenna aika, jolloin ruoka syötiin
        else:
            snake_pos.pop()  # Poista maton häntä, jos ruokaa ei syöty

        # Uusi ruoka
        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width // block_size)) * block_size,
                        random.randrange(1, (screen_height // block_size)) * block_size]
            food_spawn = True

        # Pelin rajojen tarkistus
        if snake_pos[0][0] < 0 or snake_pos[0][0] >= screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] >= screen_height:
            game_over()

        # Mato itseensä törmääminen vain, jos 10 sekuntia on kulunut ruoan syömisestä
        if time.time() - last_food_time > food_timeout:
            for block in snake_pos[1:]:
                if snake_pos[0] == block:
                    game_over()

        # Näytön päivitys
        screen.fill(blue)

        # Piirrä ruoka
        pygame.draw.rect(screen, yellow, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))

        # Piirrä mato
        for segment in snake_pos:
            pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], block_size, block_size))

        # Näytä pistemäärä
        show_score(1, white, 'comicsansms', 35)

        # Päivitä näyttö
        pygame.display.update()

        # Aseta pelin nopeus
        clock.tick(snake_speed)

# Käynnistä peli
main_game()
