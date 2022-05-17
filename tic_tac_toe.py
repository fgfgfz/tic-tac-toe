import pygame as pg
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LMB = 1


class Game:
    FPS = 60
    active_x = True
    step = 0
    winner = None

    outcomes = {
        'row_1': [],
        'row_2': [],
        'row_3': [],
        'col_1': [],
        'col_2': [],
        'col_3': [],
        'dia_1': [],
        'dia_2': [],
    }

    def __init__(self):
        self.width = 300
        self.height = 300
        self.cells = []
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Tic-tac-toe')

    @classmethod
    def append_outcomes(cls, cell, value):
        cls.outcomes[f'row_{cell.coord[0]}'].append(value)
        cls.outcomes[f'col_{cell.coord[1]}'].append(value)

        if cell.coord[0] == cell.coord[1]:
            cls.outcomes['dia_1'].append(value)
        if cell.coord == (3, 1) or cell.coord == (2, 2) or cell.coord == (1, 3):
            cls.outcomes['dia_2'].append(value)

    def fill(self, color):
        self.screen.fill(color)

    def create_cells(self):
        for row in range(3):
            for col in range(3):
                coord = (row + 1, col + 1)
                x = (100 * col)
                y = (100 * row)
                pos = (x, y)
                cell = Cell(self, coord, pos)
                self.cells.append(cell)

    def blit_cells(self):
        for cell in self.cells:
            self.screen.blit(cell.surface, cell.pos)

    def draw_grid(self):
        # TODO: переделать?
        pg.draw.line(self.screen, BLACK, (100, 0), (100, 300))
        pg.draw.line(self.screen, BLACK, (200, 0), (200, 300))
        pg.draw.line(self.screen, BLACK, (0, 100), (300, 100))
        pg.draw.line(self.screen, BLACK, (0, 200), (300, 200))

    def update_screen(self):
        self.blit_cells()
        self.draw_grid()
        pg.display.update()


class Cell:
    def __init__(self, parent, coord, pos):
        self.parent = parent
        self.width = 100
        self.height = 100
        self.coord = coord
        self.pos = pos
        self.surface = pg.Surface((self.width, self.height))
        self.surface.fill(WHITE)
        self.active = False

    def draw_x(self):
        Game.active_x = False
        pg.draw.line(self.surface, BLACK, (10, 10), (90, 90), 2)
        pg.draw.line(self.surface, BLACK, (10, 90), (90, 10), 2)
        self.parent.update_screen()

    def draw_o(self):
        Game.active_x = True
        pg.draw.circle(self.surface, BLACK, (50, 50), 45, 2)
        self.parent.update_screen()


def main():
    pg.init()
    game = Game()
    game.fill(WHITE)
    game.create_cells()
    game.update_screen()

    is_running = True

    while is_running:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == LMB:
                for cell in game.cells:

                    if (cell.pos[0] + cell.width) > event.pos[0] >= cell.pos[0] and \
                            (cell.pos[1] + cell.height) > event.pos[1] >= cell.pos[1]:

                        if not cell.active:
                            Game.step += 1
                            cell.active = True

                            if Game.active_x:
                                cell.draw_x()
                                Game.append_outcomes(cell, 'x')
                            else:
                                cell.draw_o()
                                Game.append_outcomes(cell, 'o')

                            if 9 >= Game.step >= 5:
                                for outcome in Game.outcomes.values():

                                    if len(outcome) == 3 and len(set(outcome)) == 1:
                                        Game.winner = outcome[0]

        # TODO: @classmethod и новое окно с текстом победы и кнопкой НГ
        if Game.winner:
            print(f'ПОБЕДИТЕЛЬ: {Game.winner}')
            is_running = False

        if not Game.winner and Game.step == 9:
            print(f'НИЧЬЯ :(')
            is_running = False

        game.clock.tick(game.FPS)


if __name__ == '__main__':
    main()
