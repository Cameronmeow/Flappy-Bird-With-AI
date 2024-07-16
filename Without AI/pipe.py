import pygame

#Create the pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self,x,y,position,pipe_gap):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('./Assets/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top and position -1 is from the bottom

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #flip y axis not x
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]

        if position == -1:
            self.rect.topleft=[x,y+int(pipe_gap/2)]

    def update(self,flying,game_over, scroll_speed ):
        if flying== True:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()
            
        
