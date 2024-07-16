import pygame
from pygame.locals import *
import button
import bird
import pipe
import os
import neat
import random


def main():
    
    pygame.init()
    #If no frame rate is set then it will run code as quickly as possible
    #
    clock=pygame.time.Clock()
    fps=60
    #set screen width and height
    screen_width=864
    screen_height=650

    #create game window...set to a variable called screen
    screen = pygame.display.set_mode((screen_width,screen_height)) 

    #Caption for the window(title)
    pygame.display.set_caption('Flappy Bird') 


    #Font variables
    font_score= pygame.font.SysFont('Bauhaus 93',60)
    font_end=pygame.font.SysFont('Ariel',50)
    white=(255,255,255)

    #Define Game Variables
    ground_scroll= 0 
    scroll_speed=4 # 4 pixels
    flying= False # so that it doesnt instantly starts
    game_over= False 
    start_button_clicked =False 
    exit_button_clicked =False 
    restart_button_clicked =False 
    pipe_gap=150 #initial pipe gap
    pipe_frequency= 1500 # how often pipe appears in milliseconds
    last_pipe= pygame.time.get_ticks() #check when is the last pipe created
    score= 0
    pass_pipe= False
    

    #Load the images
    background=pygame.image.load('./Assets/bg.png')
    ground=pygame.image.load('./Assets/ground.png')
    restart_img=pygame.image.load('./Assets/restart.png').convert_alpha()
    start_img=pygame.image.load('./Assets/start_btn.png').convert_alpha()
    exit_img=pygame.image.load('./Assets/exit_btn.png').convert_alpha()

    #text
    def draw_text(text,font,text_col,x,y):
        img=font.render(text,True,text_col)
        screen.blit(img,(x,y))

    #Reset_game()
    def reset_game():
        pipe_group.empty()
        flappy.rect.x= 200
        flappy.rect.y=int(screen_height/2)
        score = 0
        return score
    #Create button instances
    start_button = button.Button(int(screen_width*0.4),250,start_img,0.6)  
    exit_button = button.Button(int(screen_width*0.4)-100,250,exit_img,0.6)  
    restart_button = button.Button(int(screen_width*0.4)+120,250,restart_img,1.75)  


    pipe_group=pygame.sprite.Group()
    bird_group=pygame.sprite.Group()
    flappy = bird.Bird(200,int(screen_height/2)) #initial position 
    bird_group.add(flappy) #add this to the bird group



    run=True
    while run:


        clock.tick(fps)
        #choose game window you want to display the image and display is done via blit() function
        screen.blit(background,(0,-200))

        #Draw start button if its not clicked and the game hasnt started
        if start_button_clicked == False and flying == False and game_over == False:
            start_button_clicked = start_button.draw(screen)
        if start_button_clicked == True  and flying == False and game_over == False:    
            flying= True
            

        #Bird

        bird_group.draw(screen)
        bird_group.update(flying,game_over)

        #Pipe
        pipe_group.draw(screen)
        
        #Draw the ground
        screen.blit(ground,(ground_scroll,500))

        #Check the score 
        
        if len(pipe_group) > 0: #that means some pipes have been created
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                    pass_pipe= True
                    
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score +=1
                    pass_pipe = False
                    # print(score)
        if game_over==False:
            draw_text(str(score),font_score,white,int(screen_width/2)-20,20)
        #Look for collision with pipes
        #false,false in if group.collide() because we dont want them to be killed/deleted if the collide
        if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0: #goes above the top
            game_over= True
        if flappy.rect.bottom > 500 :
            game_over = True
            flying = False
        #Looks for collision with ground


        
        #scroll the ground if game_over==False
        if game_over == False and flying == True:
            #Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now- last_pipe > pipe_frequency:
                pipe_height = random.randint(-100,100)
                btm_pipe= pipe.Pipe(screen_width,int(screen_height/2)-50+pipe_height,-1,pipe_gap)
                top_pipe= pipe.Pipe(screen_width,int(screen_height/2)-50+pipe_height,+1,pipe_gap)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)

                last_pipe=time_now
            #Basically there is an extra 35px section in the ground, If we are about to cross that 35px mark then the ground position is reseted to zero 
            ground_scroll-=scroll_speed
            if abs(ground_scroll)>35:
                ground_scroll=0
            pipe_group.update(flying,game_over,scroll_speed) # only happend if game is running

        if game_over == True:
            draw_text("You lost. Your score is" +" " + str(score),font_end,white,int(screen_width/2)-200,20)
            if exit_button.draw(screen) == True:
                run=False

            if restart_button.draw(screen)== True:
                game_over = False
                score=reset_game()
                


        #pygame.event.get() gets all the events that is happening
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run=False
            if game_over==False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        flappy.vel = -10 

        #updates everything that happens above it
        pygame.display.update()

    #When loop ends quit the game
    pygame.quit()

main()

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p=neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)
    

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)