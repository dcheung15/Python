import pygame.display
from board import Board

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 920))
        self.clock = pygame.time.Clock()
        self.running = True
        self.speed = 50
        self.board = Board(self.screen)
        pygame.font.init()
        self.score_font = pygame.font.SysFont('Arial', 26)
        self.run()

    def run(self):
        counter = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.board.on_key_up()
                    if event.key == pygame.K_DOWN:
                        self.board.on_key_down()
                    if event.key == pygame.K_LEFT:
                        self.board.on_key_left()
                    if event.key == pygame.K_RIGHT:
                        self.board.on_key_right()
                    self.screen.fill("black")
                    self.board.update(False)
                    self.board.draw()

            if counter % self.speed == 0:
                self.board.update()
                counter = 1
                self.screen.fill("black")
                self.board.draw()

            pygame.display.flip()
            counter += 1
            self.clock.tick(40)
            text_surface = self.score_font.render('Score: ' + str(self.board.score), False, (255, 255, 255))
            self.screen.blit(text_surface, (500, 150))
        pygame.quit()
