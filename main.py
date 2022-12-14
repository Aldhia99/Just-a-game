import pygame, sys, os
from pygame.math import Vector2
from pygame import Rect

class GameState():
    
    def __init__(self) -> None:
        self.worldSize = Vector2(16,10)
        self.tankPos = Vector2(100,100)
    
    def update(self, moveTankCommand):
        self.tankPos += moveTankCommand
        
        if self.tankPos.x < 0:
            self.tankPos.x = 0
        elif self.tankPos.x >= self.worldSize.x-1:
            self.tankPos.x = self.worldSize.x -1
        
        if self.tankPos.y < 0:
            self.tankPos.y = 0
        elif self.tankPos.y >= self.worldSize.y-1:
            self.tankPos.y = self.worldSize.y -1
        
class UserInterface():
    
    def __init__(self) -> None:
                
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        self.gameState = GameState()
        
        self.cellSize = Vector2(64,64)
        self.unitsTexture = pygame.image.load("units.png")
        
        windowSize = self.gameState.worldSize.elementwise()*self.cellSize
        self.screen = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        
        pygame.display.set_caption("Tank game")
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()
        
        self.moveTankCommand = Vector2()
        self.speed = 0.1
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.moveTankCommand.y = -self.speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.moveTankCommand.y = self.speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moveTankCommand.x = self.speed
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moveTankCommand.x = -self.speed
    
    def update(self):
        self.gameState.update(self.moveTankCommand)
    
    def render(self):
        self.screen.fill((0,0,0))
        
        spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
        texturePoint = Vector2(1,0).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x),int(texturePoint.y),int(self.cellSize.x),int(self.cellSize.y))
        self.screen.blit(self.unitsTexture,spritePoint,textureRect)
        
        pygame.display.update()

    def main(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)

if __name__=="__main__":
    game = UserInterface()
    game.main()
    pygame.quit()
    sys.exit()