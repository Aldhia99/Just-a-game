import pygame, sys, os

class Game():
    
    def __init__(self) -> None:
                
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Tank game")
        
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()
        
        self.x = 100
        self.y = 100
        self.dir = ""
        self.speed = 3
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.dir = "u"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.dir = "s"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.dir = "r"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.dir = "l"
    
    def update(self):
        if self.dir == "u" and self.y>0:
            self.y -= self.speed
        elif self.dir == "s" and self.y<400:
            self.y += self.speed
        if self.dir == "r" and self.x<400:
            self.x += self.speed
        elif self.dir == "l" and self.x>0:
            self.x -= self.speed
    
    def render(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen,(0,255,0),(self.x,self.y,100,100))
        pygame.display.update()

    def main(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)

if __name__=="__main__":
    game = Game()
    game.main()
    pygame.quit()
    sys.exit()