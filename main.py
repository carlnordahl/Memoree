import random

import pygame
import time

pygame.init()

display_width = 800
display_height = 800
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("MEMOREE")

clock = pygame.time.Clock()

# variables to store time played
seconds = 0
minutes = 0

# RGB-values for colors used
black = [0, 0, 0]
red = [255, 0, 0]
white = [255, 255, 255]
light_blue = [207, 242, 252]
grey = [200, 200, 200]

# list of pressed cards coordinates to keep track of how many cards are revealed.
pressed_cards = []

# list of characters connected to cards (placeholder for icons)
icons = []

# list of images (to replace icons when working)
images = []

# intervals for x- and y-coordinates for all cards
cards_coordinates = []

# font-styles used
card_font = pygame.font.SysFont('comicsansms', 40)
button_font = pygame.font.SysFont('comicsansms', 50)
button_font_small = pygame.font.SysFont('comicsansms', 20)


def run_time():
    return str(round(pygame.time.get_ticks() / 1000))


def image_paths():

    image_paths_list = ["assets/panda.png", "assets/dog.png",
                        "assets/pizza.png", "assets/cow.png",
                        "assets/meat.png", "assets/leaf.png",
                        "assets/cat.png", "assets/monkey.png",
                        "assets/sheep.png", "assets/tomato.png"]

    duplicated_paths_list = image_paths_list + image_paths_list

    return duplicated_paths_list


# display time played/left in top center of window.
def display_time(starting_time, difficulty):
    seconds_played = round((pygame.time.get_ticks() - starting_time) / 1000)
    minutes_played = seconds_played // 60
    seconds_played = seconds_played % 60
    if difficulty == 0:
        # easy mode, count time passed
        time_played = f"{minutes_played}:{str(seconds_played).zfill(2)}"
    elif difficulty == 1:
        # medium mode, count down from 5 minutes
        if seconds_played == 0:
            # when finishing a minute
            time_played = f"{5 - minutes_played}:00"
        else:
            time_played = f"{4 - minutes_played}:{str(60 - seconds_played).zfill(2)}"
    elif difficulty == 2:
        # hard mode, count down from 1 minute
        if seconds_played == 0:
            time_played = f"{1 - minutes_played}:00"
        else:
            time_played = f"{0 - minutes_played}:{str(60 - seconds_played).zfill(2)}"
    global seconds
    global minutes
    if seconds_played != seconds:
        label(time_played, 300, 60, 200, 80, text_relative_x_pos=50)

        seconds = seconds_played
        minutes = minutes_played


def draw_card(x, y, color, border_color):
    pygame.draw.rect(display, color, [x, y, 60, 80], 0, 10)
    pygame.draw.rect(display, border_color, [x, y, 60, 80], 5, 10)


def reveal_card(coordinates):
    draw_card(coordinates[0], coordinates[2], white, black)
    # message(icons[cards_coordinates.index(coordinates)], black, coordinates[0] + 15, coordinates[2] + 20, card_font)
    image = pygame.transform.scale(pygame.image.load(images[cards_coordinates.index(coordinates)]), (40, 40))

    display.blit(image, (coordinates[0] + 10, coordinates[2] + 20))


# check if the pressed cards are matching
def matching_cards():
    if images[cards_coordinates.index(pressed_cards[0])] == images[cards_coordinates.index(pressed_cards[1])]:
        return True
    else:
        return False


def draw_all_cards():
    # draw 20 cards to play memory game with
    for row in range(4):
        for column in range(5):
            time.sleep(0.08)
            draw_card((100 + 135 * column), (200 + 155 * row), red, black)
            pygame.display.update()


def message(text, color, x, y, font):
    display.blit(font.render(text, True, color), [x, y])
    pygame.display.update()


def label(text, x, y, width, height, font=button_font, color=white, border_color=black, text_relative_x_pos=0,
          text_relative_y_pos=0):
    # MEMORY label
    pygame.draw.rect(display, color, [x, y, width, height], 0, 20)
    pygame.draw.rect(display, border_color, [x, y, width, height], 5, 20)
    message(text, black, (x + text_relative_x_pos), (y + text_relative_y_pos), font)


def game_loop(difficulty):
    game_over = False
    open_menu = False
    matches = 0

    # Reset icons
    global icons
    icons = ["A", "C", "H", "E", "6", "P", "V", "3", "L", "M", "3", "P", "E", "M", "L", "6", "V", "C", "A", "H"]
    random.shuffle(icons)

    # Reset images
    global images
    images = image_paths()
    random.shuffle(images)

    # Reset coordinates
    reset_coordinates = []
    for i in range(4):
        for y in range(5):
            reset_coordinates.append([(100 + 135 * y), (160 + 135 * y), (200 + 155 * i), (280 + 155 * i)])
    global cards_coordinates
    cards_coordinates = reset_coordinates

    display.fill(light_blue)
    if difficulty == 0:
        label("0:00", 300, 60, 200, 80, text_relative_x_pos=50)
    elif difficulty == 1:
        label("5:00", 300, 60, 200, 80, text_relative_x_pos=50)
    elif difficulty == 2:
        label("1:00", 300, 60, 200, 80, text_relative_x_pos=50)

    draw_all_cards()
    pressed_cards.clear()

    starting_time = pygame.time.get_ticks()

    while not game_over:
        display_time(starting_time, difficulty)

        # check if player lost game
        if difficulty == 1 and minutes == 5:
            game_over = True
            open_menu = True
            for card in cards_coordinates:
                reveal_card(card)
            time.sleep(1)
            # display.fill(light_blue)
            # X
            for i in range(5):
                time.sleep(0.2)
                draw_card(280 + i * 40, 250 + i * 60, red, black)
                pygame.display.update()
            for i in range(5):
                time.sleep(0.2)
                draw_card(440 - i * 40, 250 + i * 60, red, black)
                pygame.display.update()
            time.sleep(1)
        elif difficulty == 2 and minutes == 1:
            game_over = True
            open_menu = True
            for card in cards_coordinates:
                reveal_card(card)
            time.sleep(1)
            # X
            for i in range(5):
                time.sleep(0.2)
                draw_card(280 + i * 40, 250 + i * 60, red, black)
                pygame.display.update()
            for i in range(5):
                time.sleep(0.2)
                draw_card(440 - i * 40, 250 + i * 60, red, black)
                pygame.display.update()
            time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                open_menu = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_over = True
                    open_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # get position of mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # check if player has clicked on a card
                    for coordinates in cards_coordinates:
                        if coordinates[0] <= mouse_x <= coordinates[1] and coordinates[2] <= mouse_y <= coordinates[3]:
                            # make copy of pressed_cards list. To check if the clicked card had been revealed. A copy
                            # is made in order to have a version of the list where no changes has been made yet.
                            pressed_cards_copy = pressed_cards.copy()

                            # reveal card
                            reveal_card(coordinates)

                            # if 2 cards are revealed
                            if len(pressed_cards) > 1:
                                if matching_cards():
                                    matches += 1
                                    # if they're matching, remove the cards from the coordinates and icons list
                                    # they are now not in the game
                                    for card in pressed_cards:
                                        draw_card(card[0], card[2], light_blue, light_blue)
                                        images.pop(cards_coordinates.index(card))
                                        cards_coordinates.remove(card)
                                else:
                                    # if they're not matching, "flip" them over again
                                    for card in pressed_cards:
                                        draw_card(card[0], card[2], red, black)

                                pressed_cards.clear()

                            # add the pressed card to pressed_cards, unless it hasn't been revealed already
                            if coordinates not in pressed_cards_copy:
                                pressed_cards.append(coordinates)

                            # Check if player won the game:
                            if matches == 9 and len(pressed_cards) == 2:
                                game_over = True
                                open_menu = True

                                for card in pressed_cards:
                                    draw_card(card[0], card[2], light_blue, light_blue)

                                # W
                                for i in range(5):
                                    time.sleep(0.2)
                                    draw_card(40 * i + 130, 300 + (i % 2) * 40, red, black)
                                    pygame.display.update()

                                # I
                                for i in range(2):
                                    time.sleep(0.2)
                                    draw_card(40 * i + 370, 340 + (i % 2) * (-40), red, black)
                                    pygame.display.update()

                                # N
                                for i in range(4):
                                    time.sleep(0.2)
                                    draw_card(40 * i + 490, 340 + (i % 2) * (-40), red, black)
                                    pygame.display.update()

                                time.sleep(2)

        pygame.display.update()

        clock.tick(40)

    if open_menu:
        menu()


def menu():
    """
    Menu function. Has some graphics and a button that starts the game.
    Improvements: High score, difficulty (time limit, amount of cards)
    """
    menu_open = True
    start_game = False

    # 0 = unlimited time
    # 1 = 5 minutes
    # 2 = 1 minute
    difficulty = 0

    display.fill(light_blue)

    # some graphic design for menu
    for card in range(20):
        draw_card(random.randint(0, 740), random.randint(0, 720), red, black)

    # MEMORY label
    label("MEMOREE", 200, 50, 400, 100, text_relative_x_pos=75, text_relative_y_pos=20)

    # START GAME button
    label("START", 200, 200, 400, 100, text_relative_x_pos=100, text_relative_y_pos=20)

    # easy mode button
    label("EASY", 215, 305, 120, 50, font=button_font_small, text_relative_x_pos=30, text_relative_y_pos=10, color=grey)

    # medium mode button
    label("MEDIUM", 340, 305, 120, 50, font=button_font_small, text_relative_x_pos=15, text_relative_y_pos=10)

    # hard mode button
    label("HARD", 465, 305, 120, 50, font=button_font_small, text_relative_x_pos=30, text_relative_y_pos=10)

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 200 <= mouse_x <= 600 and 200 <= mouse_y <= 300:
                        menu_open = False
                        start_game = True
                    elif 215 <= mouse_x <= 335 and 305 <= mouse_y <= 355:
                        # make button grey
                        label("EASY", 215, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10, color=grey)
                        # make other buttons white
                        label("MEDIUM", 340, 305, 120, 50, font=button_font_small, text_relative_x_pos=15,
                              text_relative_y_pos=10)
                        label("HARD", 465, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10)

                        difficulty = 0
                    elif 340 <= mouse_x <= 460 and 305 <= mouse_y <= 355:
                        difficulty = 1
                        label("MEDIUM", 340, 305, 120, 50, font=button_font_small, text_relative_x_pos=15,
                              text_relative_y_pos=10, color=grey)
                        label("EASY", 215, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10)
                        label("HARD", 465, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10)

                    elif 465 <= mouse_x <= 585 and 305 <= mouse_y <= 355:
                        difficulty = 2
                        label("HARD", 465, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10, color=grey)
                        label("EASY", 215, 305, 120, 50, font=button_font_small, text_relative_x_pos=30,
                              text_relative_y_pos=10)
                        label("MEDIUM", 340, 305, 120, 50, font=button_font_small, text_relative_x_pos=15,
                              text_relative_y_pos=10)
        pygame.display.update()

        clock.tick(40)

    if start_game:
        game_loop(difficulty)


print(cards_coordinates)
menu()
pygame.quit()
