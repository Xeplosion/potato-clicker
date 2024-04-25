# Foster Cavender
# CS1400 online 7 week

import pygame
from cursor import Cursor
from food import Potato

SCREEN_WIDTH = 1280  # Use constants here to be able to use in different places
SCREEN_HEIGHT = 720
CLOCK_TICK = 30
TITLE = "Potato Master 6000"


# create critter method
def make_critters_list(count, screen, images):
    temp = []
    # probably not the best method for scaling, but since round sizes are always even it works ;)
    for i in range(0, count // 2):
        temp.append(Potato(screen, True, images[0]))
        temp.append(Potato(screen, False, images[1]))

    return temp


def main():
    # Set up the pygame window and clock
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    ##########
    # Set up game components
    poison = pygame.image.load("./assets/posion.png")
    potato = pygame.image.load("./assets/potato.png")
    grass = pygame.image.load("./assets/grass.png")

    win_sound = pygame.mixer.Sound("./assets/minecraft-rare-achievement.mp3")
    lose_sound = pygame.mixer.Sound("./assets/classic_hurt.mp3")
    creeper_sound = pygame.mixer.Sound("./assets/tnt-explosion.mp3")
    eat_sound = pygame.mixer.Sound("./assets/nom-nom-nom_gPJiWn4.mp3")
    pygame.mixer.music.load("./assets/4 - Pigstep (Mono Mix).mp3")
    pygame.mixer.music.play(-1, 0.0)

    default_font = pygame.font.get_default_font()
    font = pygame.font.Font(default_font, 32)
    win_text = font.render("You won! Congrats! Press space to restart.", True, "blue")
    win_text_rect = win_text.get_rect()
    win_text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    lose_text = font.render("NERD! You lost. Press space to restart.", True, "red")
    lose_text_rect = lose_text.get_rect()
    lose_text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    ##########

    ##########
    # Set up game data
    critter_count = 10
    critter_list = make_critters_list(critter_count, screen, [poison, potato])
    pygame.mouse.set_visible(False)

    mouse_steve = Cursor("./assets/steve.png")
    mouse_creeper = Cursor("./assets/creeper.png")

    mode = 0
    clicked = False
    ##########

    ##########
    # Game Loop
    ##########
    game_over = False
    running = True
    win = True
    tick = 0
    while running:
        ##########
        # Get Input/Events
        ##########
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicked the window's X button
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    ### Do Stuff to Reset Game ###
                    critter_list.clear()
                    critter_count = 10 + critter_count if win else 10
                    critter_list = make_critters_list(critter_count, screen, [poison, potato])

                    mode = 0
                    tick = 0
                    win = True
                    game_over = False

                    pygame.mixer.music.play(-1)

            clicked = True if event.type == pygame.MOUSEBUTTONDOWN else False

        ##########
        # Update state of components/data
        ##########
        #### Always Update ####
        mouse_steve.update_pos(pygame.mouse.get_pos())
        mouse_creeper.update_pos(pygame.mouse.get_pos())

        #### Update if Game is Not Over ####
        if not game_over:
            for i in range(0, len(critter_list)):
                # only continue past this point if user is clicking
                if clicked is False:
                    break

                # check if object has been clicked
                if critter_list[i].did_get(pygame.mouse.get_pos()):
                    # define game lose
                    if critter_list[i].poisonous and mode == 0\
                     or critter_list[i].poisonous is False and mode == 1:
                        win = False
                        game_over = True
                        critter_list.clear()
                        lose_sound.play()
                        break
                    # define successful click
                    else:
                        print("ran the success click code")
                        mode = 0 if critter_list[i].poisonous else 1
                        creeper_sound.play() if critter_list[i].poisonous else eat_sound.play()
                        critter_list.pop(i)
                        win = True
                        break

            # check if game won
            if len(critter_list) == 0:
                game_over = True
                win_sound.play()

            # update object positions
            for i in range(0, len(critter_list)):
                critter_list[i].move_potato()
                critter_list[i].draw()

            # keep track of tick for round time
            tick += 1

        #### Update if Game is Over ####
        else:
            pygame.mixer.music.stop()

        ##########
        # Update Display
        ##########
        #### Always Display ####
        screen.blit(grass, (0, 0))

        #### Display while Game is being played ####
        if not game_over:
            for i in range(0, len(critter_list)):
                critter_list[i].draw()

            if mode == 0:
                mouse_steve.draw(screen)
            else:
                mouse_creeper.draw(screen)
        #### Display while Game is Over ####
        else:
            # timer text
            time_text = font.render("You finished this round in " + str(round(tick / CLOCK_TICK, 2)) + " seconds!", True, "black")
            time_text_rect = time_text.get_rect()
            time_text_rect.center = (screen.get_width() // 2, screen.get_height() // 4 * 3)
            screen.blit(time_text, time_text_rect)

            # win / lose text
            if win:
                screen.blit(win_text, win_text_rect)
            else:
                screen.blit(lose_text, lose_text_rect)

        #### Draw changes the screen ####
        pygame.display.flip()

        ##########
        # Define the refresh rate of the screen
        ##########
        clock.tick(CLOCK_TICK)


main()
