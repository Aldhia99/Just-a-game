import pygame, sys, os, math
from pygame.math import Vector2
from pygame import Rect

class Unit():
    def __init__(self,state,position,tile):
        self.state = state
        self.position = position
        self.tile = tile
        self.orientation = 0
        self.weaponTarget = Vector2(0,0)  

class Tank(Unit):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile)

class Tower(Unit):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile) 

class Command():
    def run(self):
        raise NotImplementedError()
    
class MoveCommand(Command):
    def __init__(self,state,unit,moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
    def run(self):
        # Update unit orientation
        if self.moveVector.x < 0: 
            self.unit.orientation = 90
        elif self.moveVector.x > 0: 
            self.unit.orientation = -90
        if self.moveVector.y < 0: 
            self.unit.orientation = 0
        elif self.moveVector.y > 0: 
            self.unit.orientation = 180

        # Compute new tank position
        newPos = self.unit.position + self.moveVector

        # Don't allow positions outside the world
        if newPos.x < 0 or newPos.x >= self.state.worldWidth \
        or newPos.y < 0 or newPos.y >= self.state.worldHeight:
            return

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow other unit positions 
        for otherUnit in self.state.units:
            if newPos == otherUnit.position:
                return

        self.unit.position = newPos

class TargetCommand(Command):
    def __init__(self,state,unit,target):
        self.state = state
        self.unit = unit
        self.target = target
    def run(self):
        self.unit.weaponTarget = self.target

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
    
    def update(self,moveTankCommand,targetCommand):
        for unit in self.units:
            unit.move(moveTankCommand)
        for unit in self.units:
            unit.orientWeapon(targetCommand) 
    
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

    def renderTile(self,surface,position,tile,angle=None):
        # Location on screen
        spritePoint = position.elementwise()*self.ui.cellSize

        # Texture
        texturePoint = tile.elementwise()*self.ui.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.ui.cellWidth, self.ui.cellHeight)

        # Draw
        if angle is None:
            surface.blit(self.texture,spritePoint,textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.ui.cellWidth,self.ui.cellHeight),pygame.SRCALPHA)
            textureTile.blit(self.texture,(0,0),textureRect)
            # Rotate the surface with the tile
            rotatedTile = pygame.transform.rotate(textureTile,angle)
            # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
            spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
            spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
            # Render the rotatedTile
            surface.blit(rotatedTile,spritePoint)


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
            size = unit.weaponTarget - unit.position
            angle = math.atan2(-size.x,-size.y) * 180 / math.pi
            self.renderTile(surface,unit.position,Vector2(0,6),angle)
            
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
        
        self.commands = []
        self.playerUnit = self.gameState.units[0]
        
        self.speed = 1
        self.running = True
        
    @property
    def cellWidth(self):
        return int(self.cellSize.y)
    
    @property
    def cellHeight(self):
        return int(self.cellSize.x)

    def process_input(self):

        # Pygame events (close & keyboard)
        moveVector = Vector2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    moveVector.x = self.speed
                elif event.key == pygame.K_LEFT:
                    moveVector.x = -self.speed
                elif event.key == pygame.K_DOWN:
                    moveVector.y = self.speed
                elif event.key == pygame.K_UP:
                    moveVector.y = -self.speed

        # Keyboard controls the moves of the player's unit
        if moveVector.x != 0 or moveVector.y != 0:
            command = MoveCommand(self.gameState,self.playerUnit,moveVector)
            self.commands.append(command)

        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()                    
        targetCell = Vector2()
        targetCell.x = mousePos[0] / self.cellWidth - 0.5
        targetCell.y = mousePos[1] / self.cellHeight - 0.5
        command = TargetCommand(self.gameState,self.playerUnit,targetCell)
        self.commands.append(command)

        # Other units always target the player's unit
        for  unit in self.gameState.units:
            if unit != self.playerUnit:
                command = TargetCommand(self.gameState,unit,self.playerUnit.position)
                self.commands.append(command)
    
    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        
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