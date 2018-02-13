import pygame
from random import randint
pygame.init()

##################
# Initialization #
##################

scr_width = 450
scr_height = 650
scr_size = (scr_width,scr_height)
scr_center = (scr_width / 2, scr_height / 2)
white = (255,255,255)
black = (0,0,0)
lime = (0,255,0)
brightgreen = (200,255,160)
lightgreen = (130,235,110)
green = (50,205,50)
darkgreen = (50,142,35)
darkestgreen = (0,100,0)
red = (255,0,0)
blue = (0,0,255)
pink = (225,105,180)
skyblue = (100,210,255)
brown = (160,120,60)
darkbrown = (100,65,24)

# set screen size
screen = pygame.display.set_mode(scr_size)
# set screen name
pygame.display.set_caption("Flappy Bird")
# initialize clock
clock = pygame.time.Clock()

running = True
gameover = False
# first key pressed?
start = False
FPS = 60
playtime = 0.0
score = 0
highscore = 0
last_highscore = 0
# bird coordinates
bird_x = 150
bird_y = scr_center[1] - 50
bird_speed = 0
max_speed = 30
death_speed = 50
death_time = 0
flash = pygame.Surface(scr_size).convert_alpha()
# space between top and bottom pipes
pipe_space = 200
pipe_width = 110
pipe_speed = -5
# starting x coord for each pipe
ground_pos = scr_height - 70
groundstate = 0
pipe_init_x = scr_width
pipe1_x = pipe_init_x
pipe2_x = -1
pipe_y = randint(60, ground_pos-pipe_space-120)
pipe1_y = pipe_y
# number of frames since last jump
airtime = 0
# wing flap state
flap = 0
bird0 = pygame.image.load('data/flappy_bird0.png').convert_alpha()
bird1 = pygame.image.load('data/flappy_bird1.png').convert_alpha()
bird2 = pygame.image.load('data/flappy_bird2.png').convert_alpha()
# bird rotation state
rotation = 0
max_rotation = 30
flap_up = True

def bird(y=scr_center[1]-50, rotation=0, flap=0):
    """ Blit a bird image at Y, rotating it by ROTATION, and return its size """
    # load flappy bird image
    if round(flap) == 0:
        image = bird0
    elif round(flap) == 1:
        image = bird1
    elif round(flap) == 2:
        image = bird2
    # scale bird down to size
    image = pygame.transform.rotozoom(image, rotation, 0.08)
    # set bird position
    pos = image.get_rect(center=(150, y))
    screen.blit(image, pos)
    return image.get_rect().size

def pipe(space=pipe_space):
    """ Create 2 pipes with SPACE pixels between them, blit them to a surface, and return that surface """
    height = scr_height
    width = pipe_width


    ### TOP PIPE ###

    top = pygame.Surface((width, height))
    top.fill(red)
    top.set_colorkey(red)

    # end edge line
    pygame.draw.rect(top, black, (0, height-50, width, 45), 5)
    pygame.draw.rect(top, black, (3, height-50, 1, 45))
    pygame.draw.rect(top, green, (4, height-12, 4, 4))
    pygame.draw.rect(top, brightgreen, (8, height-12, width/2, 4))
    pygame.draw.rect(top, lightgreen, (width/2+8, height-12, width/2-17, 4))
    pygame.draw.rect(top, lightgreen, (width/2, height-12, 4, 4))
    pygame.draw.rect(top, green, (width-11, height-12, 4, 4))
    pygame.draw.rect(top, darkgreen, (width-7, height-12, 4, 4))

    # end inside
    pygame.draw.rect(top, lightgreen, (4, height-47, width/3, 35))
    pygame.draw.rect(top, brightgreen, (8, height-47, 4, 35))
    pygame.draw.rect(top, green, (width/3-5, height-47, 4, 35))
    pygame.draw.rect(top, green, (width/3+3, height-47, width-width/3-5, 35))
    pygame.draw.rect(top, darkgreen, (width-19, height-47, 4, 35))
    pygame.draw.rect(top, darkgreen, (width-11, height-47, 8, 35))

    pygame.draw.rect(top, black, (width-4, height-50, 1, 45))
    pygame.draw.rect(top, darkestgreen, (4, height-50, width-8, 4))

    # shaft
    pygame.draw.rect(top, black, (4, -4, width-8, height-49), 4)
    pygame.draw.rect(top, lightgreen, (7, 0, width/3, height-55))
    pygame.draw.rect(top, brightgreen, (11, 0, 4, height-55))
    pygame.draw.rect(top, green, (width/3-1, 0, 4, height-55))
    pygame.draw.rect(top, green, (width/3+7, 0, width-width/3-14, height-55))
    pygame.draw.rect(top, darkgreen, (width-22, 0, 4, height-55))
    pygame.draw.rect(top, darkgreen, (width-14, 0, 8, height-55))


    ### BOTTOM PIPE ###

    bot = pygame.Surface((width, height))
    bot.fill(red)
    bot.set_colorkey(red)

    # end edge line
    pygame.draw.rect(bot, black, (0, 0, width, 45), 5)
    pygame.draw.rect(bot, black, (3, 0, 1, 45))
    pygame.draw.rect(bot, black, (0, 3, width, 1))
    pygame.draw.rect(bot, green, (4, 4, 4, 4))
    pygame.draw.rect(bot, brightgreen, (8, 4, width/2, 4))
    pygame.draw.rect(bot, lightgreen, (width/2+8, 4, width/2-17, 4))
    pygame.draw.rect(bot, lightgreen, (width/2, 4, 4, 4))
    pygame.draw.rect(bot, green, (width-11, 4, 4, 4))
    pygame.draw.rect(bot, darkgreen, (width-7, 4, 4, 4))

    # end inside
    pygame.draw.rect(bot, lightgreen, (4, 8, width/3, 35))
    pygame.draw.rect(bot, brightgreen, (8, 8, 4, 35))
    pygame.draw.rect(bot, green, (width/3-5, 8, 4, 35))
    pygame.draw.rect(bot, green, (width/3+3, 8, width-width/3-5, 35))
    pygame.draw.rect(bot, darkgreen, (width-19, 8, 4, 35))
    pygame.draw.rect(bot, darkgreen, (width-11, 8, 8, 35))

    pygame.draw.rect(bot, black, (width-4, 0, 1, 45))
    pygame.draw.rect(bot, darkestgreen, (4, 43, width-8, 4))

    # shaft
    pygame.draw.rect(bot, black, (4, 48, width-8, height), 4)
    pygame.draw.rect(bot, lightgreen, (7, 51, width/3, height))
    pygame.draw.rect(bot, brightgreen, (11, 51, 4, height))
    pygame.draw.rect(bot, green, (width/3-1, 51, 4, height))
    pygame.draw.rect(bot, green, (width/3+7, 51, width-width/3-14, height))
    pygame.draw.rect(bot, darkgreen, (width-22, 51, 4, height))
    pygame.draw.rect(bot, darkgreen, (width-14, 51, 8, height))


    top = top.convert_alpha()
    bot = bot.convert_alpha()
    # set pipe surface height to 3 times the screen height to allow
    # for pipes to be blitted a full height above and below
    pipe = pygame.Surface((width, scr_height * 3))
    pipe.fill(red)
    pipe.set_colorkey(red)
    pipe = pipe.convert_alpha()
    pipe.blit(top, (0, -scr_height))
    pipe.blit(bot, (0, space))
    return pipe

# playtime string displayed as <minutes>:<seconds>
#def playtime_to_str(playtime):
#    seconds = int(playtime % 60)
#    # add a '0' before seconds if under 10
#    if seconds < 10:
#        seconds = '0' + str(seconds)
#    return "Playtime: {0}".format(str(int(playtime // 60)) + ':' + str(seconds))

# general white on black text displaying function
def write(msg, pos, x_diff=2, y_diff=3, face='04b_19', size=25):
    font = pygame.font.SysFont(face, size)
    b = font.render(msg, True, black).convert_alpha()
    w = font.render(msg, True, white).convert_alpha()
    screen.blit(b, (pos[0]+x_diff, pos[1]+y_diff))
    screen.blit(w, pos)

# centered text displaying function
def centered_write(msg, y=scr_center[1], x_offset=0, x_diff=3, y_diff=4, face='04b_19', size=30):
    font = pygame.font.SysFont(face, size)
    b = font.render(msg, True, black).convert_alpha()
    w = font.render(msg, True, white).convert_alpha()
    b_pos = b.get_rect(center=(scr_center[0]+x_offset+x_diff, y+y_diff))
    w_pos = w.get_rect(center=(scr_center[0]+x_offset, y))
    screen.blit(b, b_pos)
    screen.blit(w, w_pos)

# function to generate background
def background():
    # gradient sky
    sky = pygame.Surface((scr_width, scr_height))
    r = 0
    g = 0
    i = scr_height/100
    h = i
    while h <= scr_height*0.9:
        pygame.draw.rect(sky, (round(80+r),round(150+g),255), (0, h - i, scr_width, h))
        r += 1.2
        g += 0.9
        h += i
    return sky.convert_alpha()

    # clouds

def ground(state=0):
    ground = pygame.Surface((scr_width, scr_height-ground_pos))
    ground.fill(red)
    ground.set_colorkey(red)

    pygame.draw.rect(ground, brown, (0, 28, scr_width, scr_height-ground_pos))
    pygame.draw.rect(ground, darkbrown, (0, 22, scr_width, 6))

    pygame.draw.rect(ground, black, (0, 0, scr_width, 4))
    pygame.draw.rect(ground, brightgreen, (0, 4, scr_width, 3))
    pygame.draw.rect(ground, darkgreen, (0, 19, scr_width, 4))

    light = True
    for i in range(0, scr_width+60, 15):
        if light:
            pygame.draw.rect(ground, lightgreen, (i-state, 7, 15, 4))
            pygame.draw.rect(ground, lightgreen, (i-4-state, 11, 15, 4))
            pygame.draw.rect(ground, lightgreen, (i-8-state, 15, 15, 4))

        else:
            pygame.draw.rect(ground, green, (i-state, 7, 15, 4))
            pygame.draw.rect(ground, green, (i-4-state, 11, 15, 4))
            pygame.draw.rect(ground, green, (i-8-state, 15, 15, 4))

        light = not light

    screen.blit(ground, (0,ground_pos))

sky = background()
pipe1 = pipe()
pipe1_end = pipe1_x + pipe_width

############
# Gameplay #
############

while running:

    # blank screen
    screen.blit(sky, (0,0))
    # update playtime in top left corner
    #write(playtime_to_str(playtime), (3,1))

    # update pipes
    screen.blit(pipe1, (pipe1_x, pipe1_y))
    if pipe2_x >= 0:
        screen.blit(pipe2, (pipe2_x, pipe2_y))
    else:
        pipe2_end = 0

    ground(groundstate)

    # update bird
    bird_size = bird(bird_y, rotation, flap)
    bird_width = bird_size[0]
    bird_height = bird_size[1]

    # update score
    centered_write(str(score), y=50, size=50, x_diff=3, y_diff=4)
    write("Best: {0}".format(highscore), (5,5), size=29, x_diff=2, y_diff=3)

    if not gameover:

        # start the game if any key is pressed
        if not start:

            centered_write("Press SPACE to start jumping", size=28)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        start = True

        else:

            # get user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_SPACE:
                        airtime = 0

            # update bird speed (enforce max speed)
            bird_speed = (1.15 * airtime**1.45) - (3 * airtime) - 7
            if bird_speed < 0 and bird_speed <= -max_speed:
                bird_speed = -max_speed
            elif bird_speed > 0 and bird_speed >= max_speed:
                bird_speed = max_speed

            #update bird rotation (enforce max rotation)
            rotation = -(bird_speed * 3)
            if rotation < 0 and rotation <= -max_rotation:
                rotation = -max_rotation
            elif rotation > 0 and rotation >= max_rotation:
                rotation = max_rotation

            # update pipe positions
            pipe1_x += pipe_speed

            if pipe1_x < -110:
                pipe1_x = pipe2_x
                pipe1_y = pipe2_y
                pipe1 = pipe2
                pipe2_x = -1

            elif pipe1_x <= scr_width - 300:
                if pipe2_x < 0:
                    pipe2 = pipe()
                    pipe2_x = pipe_init_x
                    pipe2_end = pipe2_x + pipe_width
                    pipe2_y = randint(60, ground_pos-pipe_space-120)

            pipe2_x += pipe_speed

            bird_left = bird_x - bird_width/3.0
            bird_right = bird_x + bird_width/3.0
            bird_top = bird_y - bird_height/3.0
            bird_bot = bird_y + bird_height/3.0

            # update bird position (check for gameover and ceiling)
            if bird_bot + bird_speed >= ground_pos:
                bird_y = ground_pos - bird_height/3.0
                gameover = True
            elif (bird_left <= pipe1_end and bird_right >= pipe1_x) and (bird_top < pipe1_y or bird_bot > pipe1_y + pipe_space):
                gameover = True
            elif bird_top + bird_speed <= 0:
                bird_y = -35
            else:
                bird_y += bird_speed

            if pipe1_x + pipe_width/2 == bird_x:
                score += 1

            if score > highscore:
                highscore += 1

            # increase frame count
            airtime += 1

            # flap wings
            if flap_up:
                flap = (flap + 0.3)
                if round(flap - 0.1) >= 2:
                    flap_up = False
            else:
                flap = (flap - 0.3)
                if round(flap + 0.25) <= 0:
                    flap_up = True

            # update playtime clock
            playtime += clock.tick(FPS) / 1000.0
            groundstate = (groundstate + 5) % 60

    else:

        if death_time < FPS/5.0:

            flash_opacity = -(20 * death_time**2) + (130 * death_time)
            if flash_opacity <= 0:
                flash_opacity = 0
            elif flash_opacity >= 255:
                flash_opacity = 255
            flash.fill((255,255,255, flash_opacity))

            screen.blit(flash, (0,0))

            bird_speed = 0
            airtime = 15

        else:

            # update bird speed (enforce max speed)
            bird_speed = (1 * airtime**1.45) - (3 * airtime)
            if bird_speed > 0 and bird_speed >= death_speed:
                bird_speed = death_speed

            #update bird rotation (enforce max rotation)
            rotation = -(bird_speed * 3.8)
            if rotation < 0 and rotation <= -90:
                rotation = -90

            # update bird position
            if bird_y + bird_speed + bird_height/3.0 >= ground_pos:
                bird_y = ground_pos - bird_height/3.0
            else:
                bird_y += bird_speed

            if bird_y > ground_pos - bird_height:

                centered_write("Restart? (Press SPACE)", size=30, x_diff=3, y_diff=4)
                if highscore > last_highscore:
                    centered_write("New best!", y=110)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE and bird_y > ground_pos - bird_height and death_time >= FPS/5.0:
                    gameover = False
                    # first key pressed?
                    start = False
                    FPS = 60
                    playtime = 0.0
                    score = 0
                    if highscore > last_highscore:
                        last_highscore = highscore
                    # bird coordinates
                    bird_x = 150
                    bird_y = scr_center[1] - 50
                    bird_speed = 0
                    max_speed = 30
                    death_speed = 50
                    death_time = 0
                    flash = pygame.Surface(scr_size).convert_alpha()
                    # space between top and bottom pipes
                    pipe_space = 200
                    pipe_width = 110
                    pipe_speed = -5
                    # starting x coord for each pipe
                    pipe_init_x = scr_width
                    pipe1_x = pipe_init_x
                    pipe2_x = -1
                    pipe_y = randint(60, ground_pos-pipe_space-120)
                    pipe1_y = pipe_y
                    groundstate = 0
                    # number of frames since last jump
                    airtime = 0
                    # wing flap state
                    flap = 0
                    bird0 = pygame.image.load('data/flappy_bird0.png').convert_alpha()
                    bird1 = pygame.image.load('data/flappy_bird1.png').convert_alpha()
                    bird2 = pygame.image.load('data/flappy_bird2.png').convert_alpha()
                    # bird rotation state
                    rotation = 0
                    max_rotation = 30
                    flap_up = True

        # increase frame count
        if not bird_y + bird_height/3.0 + 5 >= ground_pos:
            airtime += 1

        death_time += 1

    pygame.display.flip()
