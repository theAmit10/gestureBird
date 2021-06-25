import pygame,sys,random
import cv2
import numpy as np
import taHandModule as htm
import time
import pyautogui


pyautogui.FAILSAFE = False


wCam, hCam = 640, 480
tipIds = [4, 8, 12, 16, 20]
pTime = 0  
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1 , detectionCon=0.5, trackCon=0.5)
wScr, hScr = pyautogui.size()


# for floor animination
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 700))
    screen.blit(floor_surface, (floor_x_pos + 576, 700)) # its is adding width of screen


# creating Bird
def create_bird():
    global ob_rect
    random_ob_pos = random.choice(ob_position)
    top_bird = ob_surface.get_rect(midtop = (700,random_ob_pos))
    ob_rect = ob_surface.get_rect(midtop = (700, random_ob_pos))
    return top_bird


# for movement of  ob_birds
def op_bird_move(birds):
    for bird in birds:
        bird.centerx -= 5
    return birds 


# to draw ob_bird
def op_draw_birds(birds):
    global rotate_ob
    for bird in birds:
        fipe = pygame.transform.flip(ob_surface, True, False)
        screen.blit(fipe,bird)
   
    
 
# to check collision between bird and ob_bird
def check_collision(birds): 
    global can_score
    for bird in birds:
        if bird_rect.colliderect(bird):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -300 or bird_rect.bottom >= 700:
        can_score= True 
        return False
    return  True

# to rotate bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)
    return new_bird 

# to animinate bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    bird_moving.play()
    return new_bird,new_bird_rect

# to opposite bird animination
def ob_animation():
    new_bird = ob_frames[ob_index]
    new_bird_rect = new_bird.get_rect(center = (ob_rect.centerx, ob_rect.centery))
    return new_bird, new_bird_rect

# to opposite bird rotate
def rotate_ob(bird):
    new_ob = pygame.transform.rotozoom(bird, -ob_movement * 3, 1)
    return new_ob

# to display score
def score_display(game_state): 
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))    
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:  {(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 280))
        screen.blit(high_score_surface, high_score_rect)


# to update score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# checking score
def score_check():
    global score, can_score

    if bird_list:
        for pipe in bird_list:
            if 95 < pipe.centerx < 105 and can_score:
                score +=1
                score_sound.play()
                can_score =False 
            if pipe.centerx < 0: 
                can_score = True

################################
# initializing the pygame module
##################################
pygame.init()
screen = pygame.display.set_mode((576,800)) 
clock = pygame.time.Clock() 
game_font = pygame.font.Font('04B_19.ttf',40)



###################
# GAME VARIABLE
###################
gravity = 2.00  
bird_movement = 0
ob_movement = 0
game_active = True 
score = 0
high_score = 0
can_score = True
ob_rotate = None


############################
# BACKGROUND IMAGE
############################
bg_surface = pygame.image.load('assests/ta9.png').convert() 
bg_surface = pygame.transform.scale2x(bg_surface)

###########################
# FLOOR IMAGE
###################
floor_surface = pygame.image.load('assests/g3.png').convert_alpha()
floor_x_pos = 0


###########################
# BIRD IMAGE
###########################
bird_downflip = pygame.image.load("assests/redbird-downflap.png").convert_alpha()
bird_downflip = pygame.transform.scale2x(bird_downflip)
bird_midflip = pygame.image.load("assests/redbird-midflap.png").convert_alpha()
bird_midflip = pygame.transform.scale2x(bird_midflip)
bird_upflip = pygame.image.load("assests/redbird-upflap.png").convert_alpha()
bird_upflip = pygame.transform.scale2x(bird_upflip)

bird_frames = [bird_downflip,bird_midflip,bird_upflip]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 350))

BIRDFLIP  = pygame.USEREVENT + 1 
pygame.time.set_timer(BIRDFLIP, 200)



####################################
# OPPOSITE BIRD
####################################
ob1 = pygame.image.load("assests/ob1.png").convert_alpha()
ob2 = pygame.image.load("assests/ob2.png").convert_alpha()
ob3 = pygame.image.load("assests/ob3.png").convert_alpha()
ob4 = pygame.image.load("assests/ob4.png").convert_alpha()
ob5 = pygame.image.load("assests/ob5.png").convert_alpha()
ob6 = pygame.image.load("assests/ob6.png").convert_alpha()
ob7 = pygame.image.load("assests/ob7.png").convert_alpha()
ob8 = pygame.image.load("assests/ob8.png").convert_alpha()
ob9 = pygame.image.load("assests/ob9.png").convert_alpha()
ob10 = pygame.image.load("assests/ob10.png").convert_alpha()
ob11 = pygame.image.load("assests/ob11.png").convert_alpha()
ob12 = pygame.image.load("assests/ob12.png").convert_alpha()
ob13 = pygame.image.load("assests/ob13.png").convert_alpha()
ob14 = pygame.image.load("assests/ob14.png").convert_alpha()
ob15 = pygame.image.load("assests/ob15.png").convert_alpha()
ob16 = pygame.image.load("assests/ob16.png").convert_alpha()
ob17 = pygame.image.load("assests/ob17.png").convert_alpha()

ob_frames = [ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10, ob11, ob12, ob13, ob14, ob15, ob16, ob17]
ob_index = 0
ob_surface  = ob_frames[ob_index]
ob_rect = ob_surface.get_rect(midtop = (700, 5))

#################################
# TIMMER EVENT FOR BIRD MOVEMENT
##################################
OBFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(OBFLAP, 70)


bird_list = []
OBVILLAN = pygame.USEREVENT + 1
pygame.time.set_timer(OBVILLAN, 8000)
ob_position = [500,450,200,150,1,20,5, 100]

ob_bird_height = [200, 400, 600 ]

########################
# GAME END IMAGE
########################
game_over_surface = pygame.image.load('assests/gameovero.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center= (288, 400))


##########################################
# SOUNDS
##########################################
flap_sound = pygame.mixer.Sound('assests/swoosh.wav')
death_sound = pygame.mixer.Sound('assests/tadie.wav')
score_sound = pygame.mixer.Sound('assests/tacoin.wav')
bird_moving = pygame.mixer.Sound('assests/birdmoving.wav')
score_sound_coountdown =  200  #100

#############################
# GAME LOOP
#############################
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.tafindPosition(img)

    # CHECKING USER EVENTS  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit() 


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: 
                bird_movement = 0
                bird_movement -=  16    
                flap_sound.play()
                ob_movement = 0
            if event.key == pygame.K_SPACE and game_active == False: 
                game_active = True
                bird_list.clear()
                bird_rect.center = (100,  350)
                bird_movement = 0
                score = 0 
                ob_movement = 0


        if event.type == OBVILLAN:
            bird_list.append(create_bird())
    


        if event.type == OBFLAP:
            if ob_index < 16:
                ob_index +=1
            else:
                ob_index = 0
            ob_surface, ob_rect = ob_animation()


        if event.type == BIRDFLIP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()


    screen.blit(bg_surface,(0,-200))  

    if game_active:
        # BIRD
        bird_movement += gravity 
        rotated_bird = rotate_bird(bird_surface) 
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(bird_list)


        # OB_BIRD
        ob_movement += gravity
        ob_rect.centerx += ob_movement
        bird_list = op_bird_move(bird_list)
        op_draw_birds(bird_list)
  

        # CHECKING SCORE
        score_check()
        score_display('main_game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')


#   floor
    floor_x_pos -=  5   
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(600)

    # CHECKING HAND RECONGNITION
    fingers = []
    if len(lmList) != 0:
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]: 
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)
  


        if fingers[0] == 0 and fingers[1] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[2] == 1:
            pyautogui.press('space')



    ###################
    # Frame Rate
    ###################
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)

    ###############################
    #Display
    ###############################
    cv2.imshow("Image", img)
    if(cv2.waitKey(10) & 0xFF == ord('q') ):
        break






    

    