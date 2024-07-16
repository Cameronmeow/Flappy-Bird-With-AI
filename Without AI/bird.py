import pygame

#Create the bird
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #This allows us to inherit some of the functionalities of the sprite class(blit functions are already in this class)
        self.images=[] #intialize the list
        self.index=0   # start of at index 0
        self.counter=0 #controls how fast images changes
        for num in range(1,4):
            img=pygame.image.load(f'Assets/bird{num}.png')
            height=img.get_height()
            width=img.get_width()
            bird_img=pygame.transform.scale(img,( int(width*0.6) , int(height*0.6) ))
            self.images.append(bird_img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect() #create a rectangle from boundaries of that image
        self.rect.center=[x,y]
        self.vel = 0 #initialize velocity as vel increase y coordinate of bird increase with it
        #clicking the button boosts the velocity tempotatily which makes it go higher
        self.clicked = False # A variable to ensure that the bird doesnt continuosly go up if we havent clicked it
    def update(self,flying,game_over):
        
        #Gravity
        if flying ==True:
            self.vel += 0.5
            if self.vel>8:
                self.vel=8 # if vel reaches 8 it doesnt increase further
            if self.rect.bottom <500:
                self.rect.y += int(self.vel) #we only want the bird to go down till ground

 
        if game_over==False: #we want all of this to happen only if game over is false
            #Jump // Flying up
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked =True    
                self.vel=-10
            if pygame.mouse.get_pressed()[0] == 0: #instead of looking for mouse being clicked in this  'if statement' we are looking for mouse to be released
                self.clicked = False 

            #This handles the animation    
            self.counter += 1 #increase the counter by one every interation
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1 #updates the image
                if self.index >= len(self.images):
                    self.index=0
            self.image=self.images[self.index]

            #Rotate the bird a bit when it flies up
            # first we input the image we want to rotate...so we rotate the current image
            self.image = pygame.transform.rotate(self.images[self.index],-2*self.vel) #-2 because we want it to fall downward when it is going down
        else: #if game over is true
            self.image = pygame.transform.rotate(self.images[self.index],-90)
