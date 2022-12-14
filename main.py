import pygame, sys, os

class Game():
    
    def __init__(self) -> None:
         self.x = 100
         self.y = 100
         self.dir = ""
         self.speed = 3
    
    def init(self):
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Tank game")
        
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()

    def input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.dir = "u"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.dir = "s"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.dir = "r"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.dir = "l"
    
    def update(self):
        if self.dir == "u":
            self.y -= self.speed
        elif self.dir == "s":
            self.y += self.speed
        if self.dir == "r":
            self.x += self.speed
        elif self.dir == "l":
            self.x -= self.speed
    
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
            self.clock.tick(60)

if __name__=="__main__":
    game = Game()
    game.main()