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
        self.ground = [ 
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(7,1)],
            [ Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,5), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,5), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(7,1)],
            [ Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(8,4), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,4), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)]
        ]
        self.walls = [
            [ None, None, None, None, None, None, None, None, None, Vector2(1,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(1,3), Vector2(1,1), Vector2(0,3), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(3,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, None, None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(0,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,3), Vector2(1,1), Vector2(3,3), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)]
        ]    
    
    def update(self, moveTankCommand):
        for unit in self.units:
            unit.move(moveTankCommand)
    
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        return int(self.worldSize.y)

class Layer():
    def __init__(self,ui,imageFile):
        self.ui = ui
        self.texture = pygame.image.load(imageFile)

    def renderTile(self,surface,position,tile):
        # Location on screen
        spritePoint = position.elementwise()*self.ui.cellSize

        # Texture
        texturePoint = tile.elementwise()*self.ui.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.ui.cellWidth, self.ui.cellHeight)

        # Draw
        surface.blit(self.texture,spritePoint,textureRect)

    def render(self,surface):
        raise NotImplementedError()
class ArrayLayer(Layer):
    def __init__(self,ui,imageFile,gameState,array):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.array = array

    def render(self,surface):
        for y in range(self.gameState.worldHeight):
            for x in range(self.gameState.worldWidth):
                tile = self.array[y][x]
                if not tile is None:
                    self.renderTile(surface,Vector2(x,y),tile)

class UnitsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,units):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.units = units

    def render(self,surface):
        for unit in self.units:
            self.renderTile(surface,unit.position,unit.tile)
            self.renderTile(surface,unit.position,Vector2(0,6))
            
class UserInterface():
    
    def __init__(self) -> None:
                
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        self.gameState = GameState()
        
        self.cellSize = Vector2(64,64)
        self.layers = [
            ArrayLayer(self,"ground.png",self.gameState,self.gameState.ground),
            ArrayLayer(self,"walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self,"units.png",self.gameState,self.gameState.units)
        ]
        
        windowSize = self.gameState.worldSize.elementwise()*self.cellSize
        self.screen = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        
        pygame.display.set_caption("Tank game")
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()
        
        self.moveTankCommand = Vector2()
        self.speed = 0.05
        self.running = True
        
    @property
    def cellWidth(self):
        return int(self.cellSize.y)
    
    @property
    def cellHeight(self):
        return int(self.cellSize.x)

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

        for layer in self.layers:
            layer.render(self.screen)

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