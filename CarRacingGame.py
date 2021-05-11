#Raghu Alluri
#April 2nd, 2019
#Car Racing Game
import pygame, time, random

pygame.init()
pygame.font.init()

screen_width = 800
screen_height = 600
screen_origin = (0, 0)

red = (255, 0, 0)
purple = (255, 0, 255)
chau_green = (127,255,0)
dark_green = (0, 190, 0)
white = (255, 255, 255)
black = (0, 0 ,0)
dark_red = (238,0,0)

road_width = 488
car_width = 59

line_length = 81

smash_sound = pygame.mixer.Sound('SmashSound.wav')
mainSc_music = pygame.mixer.Sound('MainScreenMusic.wav')
pygame.mixer.music.load('ArcadeMusic.wav')

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Too Fast")
clock = pygame.time.Clock()

main_car = pygame.image.load('dodgecar.png')
backgroundImg = pygame.image.load('backgroundroad.png')
crashImg = pygame.image.load('explosion.png')
lineImg = pygame.image.load('road_lines.png')
mainImg = pygame.image.load('MainScreen-TooFast.png')

#Counts the number of obstacles the player has been able to avoid
def obj_missed(num_missed):
    font = pygame.font.SysFont('Calibri', 48)
    text_surf = font.render("Avoided: " + str(num_missed), True, red)
    screen.blit(text_surf, screen_origin)

def game_level(level_number):
    level_font = pygame.font.SysFont('Calibri', 48)
    level_TextSurf = level_font.render("Level: " + str(level_number), True, black)
    screen.blit(level_TextSurf, (0, 50))

def car_crashed(x_coordinate, y_coordinate):
    screen.blit(crashImg, (x_coordinate, y_coordinate))

#This will animate then lines of the road to make it look like it is moving
def road_movement(x_coordinate_line, y_coordinate_line):
    screen.blit(lineImg, (x_coordinate_line, y_coordinate_line))

#Drawing the obstacles for the car to avoid
def objects(obj_x, obj_y, obj_w, obj_h, color):
    pygame.draw.rect(screen, color, [obj_x, obj_y, obj_w, obj_h])

#Places the Car on the screen
def car_placement(x, y):
    screen.blit(main_car, (x, y))

def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(smash_sound)

    myfont = pygame.font.SysFont('Comic Sans MS', 115)
    TextSurf = myfont.render('Game Over', False, dark_red)
    screen.blit(TextSurf, ((screen_width / 2) - 300, (screen_height / 2) - 200))

    pygame.display.update()

    time.sleep(2)

    gameLoop()

def main_screen():

    pygame.mixer.Sound.play(mainSc_music)

    main = True

    while main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(mainImg, screen_origin)

        cursor = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        pygame.draw.rect(screen, chau_green, (300, 400, 150, 50))

        if 450 > cursor[0] > 300 and 450 > cursor[1] > 400:
            pygame.draw.rect(screen, dark_green, (300, 400, 150, 50))
            if clicked[0] == 1:
                pygame.mixer.Sound.stop(mainSc_music)
                gameLoop()
        else:
            pygame.draw.rect(screen, chau_green, (300, 400, 150, 50))

        myFont = pygame.font.SysFont("Calibri", 40)
        TextSurf = myFont.render("Play Now", False, black)
        screen.blit(TextSurf, (300, 400))

        pygame.display.update()
        clock.tick(30)

#Main Game Loop function
def gameLoop():

    pygame.mixer.music.play(-1)

    #Pygame references position of object by the top left corner of the object
    x_car = (screen_width * 0.47)
    y_car = (screen_height * 0.75)

    x_car_change = 0

    obj_x_cor = random.randint(115, road_width)
    obj_y_cor = -400
    obj_y_change = 7
    obj_wid = 60
    obj_height = 126

    line_x = (road_width / 2) + 115
    line_y = 0
    line_speed = 20

    avoided = 0

    level_now = 1

    counter = 1

    leave = False

    #main Loop for the game
    while not leave:
        #Event handling loop (ex. When user exits the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_car_change = -5
                if event.key == pygame.K_RIGHT:
                    x_car_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_car_change = 0

        #Section where functiions are called / Also the Logic code group
        #They should be in an order in which the car would be blitted on top of the background
        x_car += x_car_change   #This is for moving the x-coordinate of the car left and right

        screen.blit(backgroundImg, screen_origin)

        road_movement(line_x, line_y)
        line_y += line_speed

        objects(obj_x_cor, obj_y_cor, obj_wid, obj_height, purple)
        obj_y_cor += obj_y_change
        car_placement(x_car, y_car)
        obj_missed(avoided)
        game_level(level_now)

        if x_car < 115 or x_car > (115 + road_width) - car_width:
            crash()
        if line_y > screen_height:
            line_y = 0 - line_length
        if obj_y_cor > screen_height:
            obj_y_cor = -126
            obj_x_cor = random.randint(115, (115 + road_width) - obj_wid)
            avoided += 1

        if y_car < obj_y_cor + obj_height:
            if x_car > obj_x_cor and x_car < obj_x_cor + obj_wid or x_car + car_width > obj_x_cor and x_car + car_width < obj_x_cor + obj_wid:
                car_crashed(x_car, y_car)
                crash()

        if avoided == 10 + counter:
            level_now += 1
            obj_y_change += 2
            counter += 10

        pygame.display.update()
        clock.tick(60)

main_screen()
gameLoop()
pygame.quit()
quit()
