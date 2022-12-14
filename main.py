import pygame, sys, os
from pygame.math import Vector2
from pygame import Rect

class Unit():
    def __init__(self,state,position,tile) -> None:
        self.state = state
        self.position = position
        self.tile = tile
    def move(self,moveVector):
        raise NotImplementedError()

class Tank(Unit):
    def move(self, moveVector):
        newPos = self.position + moveVector
        
        if newPos.x < 0 or newPos.x >= self.state.worldSize.x-1 \
        or newPos.y < 0 or newPos.y >= self.state.worldSize.y-1:
            return
        
        for unit in self.state.units:
            if newPos == unit.position:
                return
        
        self.position = newPos

class Tower(Unit):
    def move(self,moveVector):
        pass

class GameState():
    
    def __init__(self) -> None:
        self.worldSize = Vector2(16,10)
        self.units = [
            Tank(self,Vector2(5,4),Vector2(1,0)),
            Tower(self,Vector2(10,3),Vector2(0,1)),
            Tower(self,Vector2(10,5),Vector2(0,1))
        ]
    
    def update(self, moveTankCommand):
        for unit in self.units:
            unit.move(moveTankCommand)
        
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
        self.speed = 0.05
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
    
    def renderUnit(self, unit):
        spritePoint = unit.position.elementwise()*self.cellSize
        
        texturePoint = unit.tile.elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x),int(texturePoint.y),int(self.cellSize.x),int(self.cellSize.y))
        self.screen.blit(self.unitsTexture,spritePoint,textureRect)
        
        texturePoint = Vector2(0,6).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x),int(texturePoint.y),int(self.cellSize.x),int(self.cellSize.y))
        self.screen.blit(self.unitsTexture,spritePoint,textureRect)
    
    def render(self):
        self.screen.fill((0,0,0))
        
        for unit in self.gameState.units:
            self.renderUnit(unit)
        
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