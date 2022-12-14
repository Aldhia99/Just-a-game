import pygame, sys

class Game():
    
    def __init__(self) -> None:
         pass
    
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))

    def input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    def update():
        pass
    
    def render():
        pass

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