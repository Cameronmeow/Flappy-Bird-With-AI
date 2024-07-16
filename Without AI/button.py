import pygame


#Create the button
class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image=pygame.transform.scale(image,( int(width*scale) , int(height*scale) ))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked = False

    def draw(self,surface):
        action=False
        #Get mouse position
        pos = pygame.mouse.get_pos()
        
        #Check mouse if it is over the button and clicked conditions
        if self.rect.collidepoint(pos):
             # is the mouse cursor colliding with the buttton rectangle
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                # print('Clicked')
                action = True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False

        #draw button on screen
        surface.blit(self.image,(self.rect.x,self.rect.y))

        return action