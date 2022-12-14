import pygame, sys, os

class Game():
    
    def __init__(self) -> None:
         self.x = 100
         self.y = 100
    
    def init(self):
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))

    def input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.y -= 10
            elif event.key == pygame.K_DOWN:
                self.y += 10
            elif event.key == pygame.K_RIGHT:
                self.x += 10
            elif event.key == pygame.K_LEFT:
                self.x -= 10
    
    def update(self):
        pass
    
    def render(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen,(0,255,0),(self.x,self.y,100,100))
        pygame.display.update()

    def main(self):
        self.init()
        while True:
            for event in pygame.event.get():
                self.input(event)
            self.update()
            self.render()

if __name__=="__main__":
    game = Game()
    game.main()