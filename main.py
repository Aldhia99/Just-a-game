import pygame, sys, os, math
from pygame.math import Vector2
from pygame import Rect

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameItem():
    def __init__(self,state,position,tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0  
        
class Unit(GameItem):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile)
        self.weaponTarget = Vector2(0,0)
        self.lastBulletEpoch = -100

class Bullet(GameItem):
    def __init__(self,state,unit):
        super().__init__(state,unit.position,Vector2(2,1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget 

class Tank(Unit):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile)

class Tower(Unit):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile) 

class GameState():
    
    def __init__(self) -> None:
        self.epoch = 0
        self.worldSize = Vector2(16,10)
        self.units = [
            Unit(self,Vector2(1,9),Vector2(1,0)),
            Unit(self,Vector2(6,3),Vector2(0,2)),
            Unit(self,Vector2(6,5),Vector2(0,2)),
            Unit(self,Vector2(13,3),Vector2(0,1)),
            Unit(self,Vector2(13,6),Vector2(0,1))
        ]
        self.ground = [ 
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(6,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,5), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,5), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,4), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(7,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)]
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
        self.bullets = [
        ]
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 10  
        
        self.observers = [
        ]
    
    @property
    def worldWidth(self):
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        return int(self.worldSize.y)
    
    def isInside(self,position):
        """
        Returns true is position is inside the world
        """
        return position.x >= 0 and position.x < self.worldWidth \
           and position.y >= 0 and position.y < self.worldHeight
    
    def findUnit(self,position):
        """
        Returns the index of the first unit at position, otherwise None.
        """
        for unit in self.units:
            if  int(unit.position.x) == int(position.x) \
            and int(unit.position.y) == int(position.y):
                return unit
        return None
    
    def findLiveUnit(self,position):
        """
        Returns the index of the first live unit at position, otherwise None.
        """
        unit = self.findUnit(position)
        if unit is None or unit.status != "alive":
            return None
        return unit 
    
    def addObserver(self,observer):
        """
        Add a game state observer. 
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)
        
    def notifyUnitDestroyed(self,unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)

class GameStateObserver():
    def unitDestroyed(self,unit):
        pass
class Command():
    def run(self):
        raise NotImplementedError()
    
class MoveCommand(Command):
    def __init__(self,state,unit,moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
    def run(self):
        unit = self.unit
        
        # Destroyed units can't move
        if unit.status != "alive":
            return
        
        # Update unit orientation
        if self.moveVector.x < 0: 
            unit.orientation = 90
        elif self.moveVector.x > 0: 
            unit.orientation = -90
        if self.moveVector.y < 0: 
            unit.orientation = 0
        elif self.moveVector.y > 0: 
            unit.orientation = 180
        
        # Compute new tank position
        newPos = unit.position + self.moveVector

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow other unit positions 
        unitIndex = self.state.findUnit(newPos)
        if not unitIndex is None:
                return

        unit.position = newPos

class TargetCommand(Command):
    def __init__(self,state,unit,target):
        self.state = state
        self.unit = unit
        self.target = target
    def run(self):
        self.unit.weaponTarget = self.target

class ShootCommand(Command):
    def __init__(self,state,unit):
        self.state = state
        self.unit = unit

    def run(self):
        if self.unit.status != "alive":
            return
        if self.state.epoch-self.unit.lastBulletEpoch < self.state.bulletDelay:
            return
        self.unit.lastBulletEpoch = self.state.epoch
        self.state.bullets.append(Bullet(self.state,self.unit))

class MoveBulletCommand(Command):
    def __init__(self,state,bullet):
        self.state = state
        self.bullet = bullet

    def run(self):
        direction = (self.bullet.endPosition - self.bullet.startPosition).normalize()
        newPos = self.bullet.position + self.state.bulletSpeed * direction
        newCenterPos = newPos + Vector2(0.5,0.5)
        # If the bullet goes outside the world, destroy it
        if not self.state.isInside(newPos):
            self.bullet.status = "destroyed"
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction.x > 0 and newPos.x >= self.bullet.endPosition.x) \
        or (direction.x < 0 and newPos.x <= self.bullet.endPosition.x)) \
        and ((direction.y >= 0 and newPos.y >= self.bullet.endPosition.y) \
        or (direction.y < 0 and newPos.y <= self.bullet.endPosition.y)):
            self.bullet.status = "destroyed"
            return
        # If the bullet is outside the allowed range, destroy it
        if newPos.distance_to(self.bullet.startPosition) >= self.state.bulletRange:  
            self.bullet.status = "destroyed"
            return
        # If the bullet hits a unit, destroy the bullet and the unit 
        unit = self.state.findLiveUnit(newCenterPos)
        if not unit is None and unit != self.bullet.unit:
            self.bullet.status = "destroyed"
            unit.status = "destroyed"
            self.state.notifyUnitDestroyed(unit)
            return
        # Nothing happends, continue bullet trajectory
        self.bullet.position = newPos

class DeleteDestroyedCommand(Command)       :
    def __init__(self,itemList):
        self.itemList = itemList

    def run(self):
        newList = [ item for item in self.itemList if item.status == "alive" ]
        self.itemList[:] = newList 


class Layer(GameStateObserver):
    def __init__(self,cellSize,imageFile):
        self.cellSize = cellSize
        self.texture = pygame.image.load(imageFile)
        
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)  
    
    def unitDestroyed(self,unit):
        pass      
        
    def renderTile(self,surface,position,tile,angle=None):
        # Location on screen
        spritePoint = position.elementwise()*self.cellSize
        
        # Texture
        texturePoint = tile.elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.cellWidth, self.cellHeight)
        
        # Draw
        if angle is None:
            surface.blit(self.texture,spritePoint,textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.cellWidth,self.cellHeight),pygame.SRCALPHA)
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
    def __init__(self,ui,imageFile,gameState,array,surfaceFlags=pygame.SRCALPHA):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags

    def render(self,surface):
        if self.surface is None:
            self.surface = pygame.Surface(surface.get_size(),flags=self.surfaceFlags)
            for y in range(self.gameState.worldHeight):
                for x in range(self.gameState.worldWidth):
                    tile = self.array[y][x]
                    if not tile is None:
                        self.renderTile(self.surface,Vector2(x,y),tile)
        surface.blit(self.surface,(0,0))

class UnitsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,units):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.units = units
        
    def render(self,surface):
        for unit in self.units:
            self.renderTile(surface,unit.position,unit.tile,unit.orientation)
            if unit.status == "alive":
                size = unit.weaponTarget - unit.position
                angle = math.atan2(-size.x,-size.y) * 180 / math.pi
                self.renderTile(surface,unit.position,Vector2(0,6),angle)

class BulletsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,bullets):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.bullets = bullets

    def render(self,surface):
        for bullet in self.bullets:
            if bullet.status == "alive":
                self.renderTile(surface,bullet.position,bullet.tile,bullet.orientation)

class ExplosionsLayer(Layer):
    def __init__(self,ui,imageFile):
        super().__init__(ui,imageFile)
        self.explosions = []
        self.maxFrameIndex = 27

    def add(self,position):
        self.explosions.append({
            'position': position,
            'frameIndex': 0
        })

    def unitDestroyed(self,unit):
        self.add(unit.position)

    def render(self,surface):
        for explosion in self.explosions:
            frameIndex = math.floor(explosion['frameIndex'])
            self.renderTile(surface,explosion['position'],Vector2(frameIndex,4))
            explosion['frameIndex'] += 0.5
        self.explosions = [ explosion for explosion in self.explosions if explosion['frameIndex'] < self.maxFrameIndex ]
            
class UserInterface():
    
    def __init__(self) -> None:
                
        pygame.init()
        
        self.gameState = GameState()
        
        self.cellSize = Vector2(64,64)
        
        windowSize = self.gameState.worldSize.elementwise()*self.cellSize
        self.screen = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        
        pygame.display.set_caption("Tank game")
        logo = pygame.image.load("tank.png")
        pygame.display.set_icon(logo)
        
        self.layers = [
            ArrayLayer(self.cellSize,"ground.png",self.gameState,self.gameState.ground,0),
            ArrayLayer(self.cellSize,"walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self.cellSize,"units.png",self.gameState,self.gameState.units),
            BulletsLayer(self.cellSize,"explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.cellSize,"explosions.png")
        ]
          
        for layer in self.layers:
            self.gameState.addObserver(layer)
        
        self.commands = []
        self.playerUnit = self.gameState.units[0]
        
        self.speed = 1
        
        self.clock = pygame.time.Clock()
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
        mouseClicked = False
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClicked = True

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

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(self.gameState,self.playerUnit)
            )
        
         # Other units always target the player's unit and shoot if close enough
        for unit in self.gameState.units:
            if unit != self.playerUnit:
                command = TargetCommand(self.gameState,unit,self.playerUnit.position)
                self.commands.append(command)
                distance = unit.position.distance_to(self.playerUnit.position)
                if distance <= self.gameState.bulletRange:
                    self.commands.append(ShootCommand(self.gameState,unit))

        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(
                MoveBulletCommand(self.gameState,bullet)
            )

        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(self.gameState.bullets)
        )
    
    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1
        
    def render(self):
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