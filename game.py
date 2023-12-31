import pygame
from pygame.locals import *
import random

#Makes pairs of pipes with the same x location of varying heights
class Pipe_Pair:
    def __init__(self,screen_width,screen_height,pan_speed,pipe_width):
        vertical_gap_size = random.randint(150, screen_height//3)
        self.x = screen_width
        #ensure that the lower pipe's top is witin the lower 3/4 of the screen while keeping enough room for top pipe
        self.low_y = random.randint(min((screen_height*9)//10, vertical_gap_size+100), screen_height-100)
        self.high_y = self.low_y - vertical_gap_size
        self.pan_speed = pan_speed
        self.pipe_width = pipe_width

    def increment(self):
        #returns False if the pipes can't move, indicating that it should be destroyed b/c off screen
        if self.x > -self.pipe_width:
            self.x -= self.pan_speed
            return True
        return False
    
    def get_loc(self):
        return self.x, self.low_y, self.high_y
def game():
    pygame.init()
    clock = pygame.time.Clock()

    #initializations
    fps = 60
    pan_speed = 3
    player_top_left_loc = (100, 325)
    screen_width = 600
    screen_height = 800
    pipe_width = 110
    pipes = []
    screen = pygame.display.set_mode([screen_width, screen_height])
    gravity = 5
    player_vel = gravity
    #Start of game loop
    running = True
    while running:

        screen.fill((20, 20, 20))  
        #bird = pygame.Surface((60,60),pygame.SRCALPHA)
        #pygame.draw.circle(bird, (0, 0, 0), (30, 30), 30)
        background = pygame.image.load("./images/Background.png").convert()

        bird = (pygame.image.load("./images/Dragon.png").convert_alpha())

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_vel = -10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_vel = gravity      
                    

        #if there are no pipes, make one immediately
        if len(pipes) == 0:
            pipes.append(Pipe_Pair(screen_width,screen_height,pan_speed,pipe_width))
        else:
            del_pipe = False
            for i in range(len(pipes)):
                if pipes[i].increment()==False:
                    del_pipe = True
            if del_pipe:
                del pipes[0]
            if screen_width-pipes[-1].get_loc()[0] > 300:
                if random.randint(0, 10)<1:
                    pipes.append(Pipe_Pair(screen_width,screen_height,pan_speed,pipe_width))
        screen.blit(background,(0,0))
        player_top_left_loc = (player_top_left_loc[0],player_top_left_loc[1]+player_vel)
        screen.blit(bird,player_top_left_loc)

        pipe_displays = []
        for pipe in pipes:
            x, low_y, high_y = pipe.get_loc()
            #pipe_displays.append(pygame.Surface((pipe_width, screen_height-low_y)))
            pipe_displays.append(pygame.image.load("./images/final_floor.png").convert())
            #pipe_displays[-1].fill((76,153,0))
            #pipe_displays.append(pygame.Surface((pipe_width, high_y)))
            pipe_displays.append(pygame.image.load("./images/final_ceiling.png").convert())
            #pipe_displays[-1].fill((76,153,0))
            screen.blit(pipe_displays[-2], (x, low_y))
            screen.blit(pipe_displays[-1], (x, -pipe_displays[-1].get_height()+high_y))
        # Flip the display
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__": 
    game()