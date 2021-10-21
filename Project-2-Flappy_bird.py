import random   #For random (occurance of pipes to make the game enjoyable
import sys      # We will use (sys.exit) to exit from program
import pygame  
from pygame.locals import *       #Basic pygame imports

#Global Variables for the Game to be declared that will remain constant throughout...
FPS = 32        #Means frame per sec for how fast we render images on the screen
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH ,SCREENHEIGHT))  #Initialises a window/screen for display of game..

GROUNDY = (SCREENHEIGHT * 0.8)     #Vertical height of the the base/ground of game...
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'E:/gallery/sprites/bird.png'       #Path of the player's/bird icon...
BACKGROUND = 'E:/gallery/sprites/background1.jpg'  
PIPE = 'E:/gallery/sprites/pipe.png'

def welcomeScreen():
    """Shows welcome image on the screen"""
    #player is --> bird
    playerx  = int(SCREENWIDTH / 5)
    playery  = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2) # GAME_SPRITES['player'].get_height() is the height of image --> of bird
    messagex = int((SCREENWIDTH  - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)   
    basex = 0

    while True:

        for event in pygame.event.get():    #It consists of all pygame events 

          # If user clicks on cross button, close the game..
          if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):    #--->Keydown means any key pressed --> that is escape
             pygame.quit()
             sys.exit()

          # If the user presses space or up key, start the game for them.
          elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
              return                 #Means go back to main and execute mainGame function..

    #Means else statement is executed nevertheless And any action by us is based on if/elif statements afterwards
          else:
              SCREEN.blit(GAME_SPRITES['background'] ,(0 ,0))   
              SCREEN.blit(GAME_SPRITES['player']     ,( playerx,playery))   
              SCREEN.blit(GAME_SPRITES['message']    ,(messagex ,messagey))   
              SCREEN.blit(GAME_SPRITES['base']       ,(basex ,GROUNDY))     #Base should be blitted after background as it comes over /overlap over background              
              pygame.display.update()     #Without this you can't change/present screen irrespective of no. of the blit u run...
              FPSCLOCK.tick(FPS)          #Means pass FPS = 32 and tick/set that.


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH /5)
    playery = int(SCREENWIDTH /2)
    basex = 0 

    #Create two pipes two for blitting on the screen  --> by using random module as pipes can be created at any instance and size
    newPipe1 = getRandomPipe()    
    newPipe2 = getRandomPipe()

    #List of [upper pipes](dictionary) on the screen 
    upperPipes = [
          {'x' : SCREENWIDTH  + 200  ,'y' : newPipe1[0]['y'] },
          {'x' : SCREENWIDTH + 200 + (SCREENWIDTH / 2) ,'y' : newPipe2[0]['y']},
    ]
    #List of [lower pipes] on the screen
    lowerPipes = [
          {'x' :SCREENWIDTH + 200  ,'y' : newPipe1[1]['y'] } ,
          {'x' :SCREENWIDTH + 200 + (SCREENWIDTH / 2) ,'y' : newPipe2[1]['y']},
    ]

    pipevelo_X = -4      #Means pipe moves in left direction

    playerVel_Y = -9     #Neeche gerega iss velocity se bird
    playerMaxVel_Y = 10     #Player is bird here is its upward velocity which is greater than its falling velocity
    playerMinVel_Y = -8
    playerAcc_Y = 1
    
    playerVel_X = -8           # Velocity of bird while flappping
    player_Flapped = False     # It is true only when the bird is flapping
   
    while (True):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVel_Y = playerVel_X
                    player_Flapped = True
                    GAME_SOUNDS['wing'].play()             # Playing the wing loaded sounds in the if the game starts 

        crash_Test = isCollide(playerx ,playery ,upperPipes ,lowerPipes)           #It returns true if the bird crashes.
        if crash_Test:
            return          #If it comes true then return none and game over and stops

       #Check for Score     
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2         #Its the the centre of the player/bird

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2    
               
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:             #Don't use brackets here otherwise score will be distubed
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()

        if playerVel_Y < playerMaxVel_Y and not player_Flapped:         #If its velocity is not max than accelerating the bird 
            playerVel_Y += playerAcc_Y
        
        if player_Flapped:                              #Means flapped once turn it back to false again              
            player_Flapped = False

        player_Height = GAME_SPRITES['player'].get_height()    
        # For below line u can open the video from time -> 1:29:01 
        playery = playery + min(playerVel_Y ,GROUNDY - playery - player_Height)    #Changing the player's 'y' co-ordinate and setting to consider minimum between any of -> PlayerVelY or min(GROUNDY..-..) 

        #Move pipes to the left
        for upperPipe ,lowerPipe in zip(upperPipes ,lowerPipes):
            upperPipe['x'] += pipevelo_X       #Moving the pipe in left direction as pipevelo_X is (-ve) by using loop
            lowerPipe['x'] += pipevelo_X       #Sme for the lower pipe

        # Add a new pipe when the first is about to cross to the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:  #Means if the pipe's position is almost to the leftmost then append new pipe by function
            nwi_Pipe = getRandomPipe()
            upperPipes.append(nwi_Pipe[0])
            lowerPipes.append(nwi_Pipe[1])
        #If the pipe is out of the screen to the left, remove it
        if upperPipes[0]['x'] < (-GAME_SPRITES['pipe'][0].get_width()):  # Its like when the pipe surpass the reference x axis from left and we remove it
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Lets blit our sprites now..
        SCREEN.blit(GAME_SPRITES['background'] ,(0 ,0))
        for upperPipe ,lowerPipe in zip(upperPipes ,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0] , (upperPipe['x'] ,upperPipe['y']))    #Bliting upper pipes 
            SCREEN.blit(GAME_SPRITES['pipe'][1] , (lowerPipe['x'] ,lowerPipe['y']))    #Bliting lower pipes 
        SCREEN.blit(GAME_SPRITES['base'] ,(basex ,GROUNDY))    
        SCREEN.blit(GAME_SPRITES['player'] ,(playerx ,playery))    

        my_Score = [int(x) for x in list(str(score))]      #MAKING A LIST 
        width = 0
        for i in my_Score:   #Iterating in the list
            width += GAME_SPRITES['numbers'][i].get_width()  # 'i' -> Iterates every single game sprites number's -> width 

        Xoffset = (SCREENWIDTH - width) / 2    #Setting up width of Score on screen

        #Now blitting the Scores on the screen
        for digit in my_Score:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()   #Just making Xoffset = (SCREENWIDTH - width) / 2  incremented by number's width
        pygame.display.update()     
        FPSCLOCK.tick(FPS)  

def isCollide(playerx, playery, upperPipes, lowerPipes):
        if (playery > GROUNDY - 25)  or (playery < 0):         #If player/bird hits the ground or upper wall 
            GAME_SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = GAME_SPRITES['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):   #If bird 'y' is less tham pipe's 'y' and bird 'x' comes inside pipe kind off then--> hit
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if(playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True

        return False

def getRandomPipe():
    """Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen"""    
    pipeHeight  = GAME_SPRITES['pipe'][0].get_height()      #Seedhe wala yaan ulta can be choosed as they have same height ..say using seedha wala from GAME_SPRITES['pipe'][0] 
    offset = SCREENHEIGHT / 3   # <-----------------------------------------------------IMP

    y2 = offset + random.randrange(0 , int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))     #y cordinate of lower pipe
    pipeX_cordinate = SCREENWIDTH + 10         #It is same for both pipes 
    y1 = pipeHeight - y2 + offset     #y cordinate of upper pipe

    pipe = [
           {'x' :pipeX_cordinate ,'y' : -y1},    # upper pipe [0]
           {'x' :pipeX_cordinate ,'y' :  y2}     #lower pipe [1]
    ]

    return pipe         #Returning the list of co-ordinates of upper and lower pipes

if __name__ == '__main__':
     # This will be the main point from where our game will start.....................>
    pygame.init()                  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock() #This time.Clock() acts as a function to control fps...
    pygame.display.set_caption('|Chetelise| - Flappy Bird')

                                # GAME SPRITES
    GAME_SPRITES['numbers'] = (  #Load the images to dictionary in a single key..using tuples
        pygame.image.load('E:/gallery/sprites/0.png').convert_alpha(), #.convert_alpha() function is like to optimize/quick blitting the image for games
        pygame.image.load('E:/gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('E:/gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message']    = pygame.image.load('E:/gallery/sprites/message.jpg').convert_alpha()       #Adding another key in the dictionary
    GAME_SPRITES['base']       = pygame.image.load('E:/gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']     = pygame.image.load(PLAYER).convert_alpha()

# Again adding a (tuple key having two elements) in the dicitonary
    GAME_SPRITES['pipe']  = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha() ,180) ,  #Roating the image 180 deg 
                            pygame.image.load(PIPE).convert_alpha()                                 #Same image unrotated
                            )
                            
                                #GAME SOUNDS adding elements
    GAME_SOUNDS['die']    = pygame.mixer.Sound('E:/gallery/audio/die.wav')
    GAME_SOUNDS['hit']    = pygame.mixer.Sound('E:/gallery/audio/hit.wav')
    GAME_SOUNDS['point']  = pygame.mixer.Sound('E:/gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('E:/gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing']   = pygame.mixer.Sound('E:/gallery/audio/wing.wav')

    while(True):
        welcomeScreen()   # Shows welcome screen to the user until he presses a button
        mainGame()   