import pygame, sys, os

class GameState():
    
    def __init__(self) -> None:
        self.x = 100
        self.y = 100
    
    def update(self, moveCommandX, moveCommandY):
        self.x += moveCommandX
        self.y += moveCommandY
        
class Game():
    
    def __init__(self) -> None:
                
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption("Tank game")
        
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()
        
        self.gameState = GameState()
        self.moveCommandX = 0
        self.moveCommandY = 0
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
                    self.moveCommandY = -self.speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moveCommandY = self.speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moveCommandX = self.speed
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moveCommandX = -self.speed
    
    def update(self):
        self.gameState.update(self.moveCommandX,self.moveCommandY)
    
    def render(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen,(0,255,0),(self.gameState.x,self.gameState.y,100,100))
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