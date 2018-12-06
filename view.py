import pygame

class View():
    def __init__(self, model, screen):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height) """
        self.model = model
        self.screen = screen

    def draw(self, screenx):
        """ Draw the current game state to the screen """
#        if self.model.endGame == False:
#            for i in range(screenx):
#                pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,700))
        self.model.appear(self.screen)
        if self.model.endGame:
            for i in range(screenx):
                    pygame.draw.line(self.screen,(i/8+40,0,0),(i,0),(i,700))
        pygame.display.update()
