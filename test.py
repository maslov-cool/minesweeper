import pygame
import random


class Minesweeper:
    # создание поля
    def __init__(self, width_, height_, quality):
        self.width = width_
        self.height = height_
        self.board = [[[0, False, -1] for _ in range(width_)] for _ in range(height_)]
        for _ in range(quality):
            self.board[random.randrange(self.height)][random.randrange(self.width)] = [0, True, 10]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][-1] == -1:

                    if not i and not j:

                        self.board[i][j][0] = sum([self.board[i + 1][j][-2], self.board[i][j + 1][-2],
                                                   self.board[i + 1][j + 1][-2]])

                    elif i == self.height - 1 and not j:

                        self.board[i][j][0] = sum([self.board[i - 1][j][-2], self.board[i][j + 1][-2],
                                                   self.board[i - 1][j + 1][-2]])

                    elif i == self.height - 1 and j == self.width - 1:

                        self.board[i][j][0] = sum([self.board[i - 1][j][-2], self.board[i][j - 1][-2],
                                                   self.board[i - 1][j - 1][-2]])

                    elif not i and j == self.width - 1:

                        self.board[i][j][0] = sum([self.board[i + 1][j][-2], self.board[i][j - 1][-2],
                                                   self.board[i + 1][j - 1][-2]])

                    elif not i and 0 < j < self.width - 1:

                        self.board[i][j][0] = sum([self.board[i + 1][j][-2], self.board[i + 1][j + 1][-2],
                                                   self.board[i + 1][j - 1][-2], self.board[i][j + 1][-2],
                                                   self.board[i][j - 1][-2]])

                    elif i == self.height - 1 and 0 < j < self.width - 1:

                        self.board[i][j][0] = sum([self.board[i - 1][j][-2], self.board[i - 1][j + 1][-2],
                                                   self.board[i - 1][j - 1][-2], self.board[i][j + 1][-2],
                                                   self.board[i][j - 1][-2]])

                    elif 0 < i < self.height - 1 and not j:

                        self.board[i][j][0] = sum([self.board[i + 1][j][-2], self.board[i - 1][j][-2],
                                                   self.board[i + 1][j + 1][-2], self.board[i - 1][j + 1][-2],
                                                   self.board[i][j + 1][-2]])

                    elif 0 < i < self.height - 1 and j == self.width - 1:

                        self.board[i][j][0] = sum([self.board[i - 1][j][-2], self.board[i + 1][j][-2],
                                                   self.board[i - 1][j - 1][-2], self.board[i + 1][j - 1][-2],
                                                   self.board[i][j - 1][-2]])

                    else:

                        self.board[i][j][0] = sum([self.board[i - 1][j - 1][-2], self.board[i - 1][j][-2],
                                                   self.board[i - 1][j + 1][-2], self.board[i][j - 1][-2],
                                                   self.board[i][j + 1][-2], self.board[i + 1][j - 1][-2],
                                                   self.board[i + 1][j][-2], self.board[i + 1][j + 1][-2]])

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen_):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][-2]:
                    if self.board[i][j][-1] == 10:
                        pygame.draw.rect(screen_, 'red',
                                         [self.left + self.cell_size * j + 1, self.top + self.cell_size * i + 1,
                                          self.cell_size - 1, self.cell_size - 1])
                    else:
                        font = pygame.font.Font(None, 25)
                        text = font.render(str(self.board[i][j][0]), True, (100, 255, 100))
                        screen.blit(text, (self.left + self.cell_size * j + 2, self.top + self.cell_size * i + 2))
                pygame.draw.rect(screen_, 'white', [self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                    self.cell_size, self.cell_size], 1)

    def get_cell(self, mouse_pos: tuple):
        if (not self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width or
                not self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height):
            return None
        else:
            return (mouse_pos[1] - self.top) // self.cell_size, (mouse_pos[0] - self.left) // self.cell_size

    def on_click(self, cell):
        if not self.board[cell[0]][cell[1]][-2]:
            if not self.board[cell[0]][cell[1]][0]:
                self.empty_cells(cell[0], cell[1])
            else:
                self.board[cell[0]][cell[1]][-2] = True

    def empty_cells(self, i, j):
        self.board[i][j][1] = True
        if not i and not j:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

            if self.board[i + 1][j + 1][0]:
                self.board[i + 1][j + 1][1] = True
            else:
                if not self.board[i + 1][j + 1][1]:
                    self.empty_cells(i + 1, j + 1)

        elif i == self.height - 1 and not j:

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

            if self.board[i - 1][j + 1][0]:
                self.board[i - 1][j + 1][1] = True
            else:
                if not self.board[i - 1][j + 1][1]:
                    self.empty_cells(i - 1, j + 1)

        elif i == self.height - 1 and j == self.width - 1:

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

            if self.board[i - 1][j - 1][0]:
                self.board[i - 1][j - 1][1] = True
            else:
                if not self.board[i - 1][j - 1][1]:
                    self.empty_cells(i - 1, j - 1)

        elif not i and j == self.width - 1:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

            if self.board[i + 1][j - 1][0]:
                self.board[i + 1][j - 1][1] = True
            else:
                if not self.board[i + 1][j - 1][1]:
                    self.empty_cells(i + 1, j - 1)

        elif not i and 0 < j < self.width - 1:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i + 1][j + 1][0]:
                self.board[i + 1][j + 1][1] = True
            else:
                if not self.board[i + 1][j + 1][1]:
                    self.empty_cells(i + 1, j + 1)

            if self.board[i + 1][j - 1][0]:
                self.board[i + 1][j - 1][1] = True
            else:
                if not self.board[i + 1][j - 1][1]:
                    self.empty_cells(i + 1, j - 1)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

        elif i == self.height - 1 and 0 < j < self.width - 1:

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i - 1][j + 1][0]:
                self.board[i - 1][j + 1][1] = True
            else:
                if not self.board[i - 1][j + 1][1]:
                    self.empty_cells(i - 1, j + 1)

            if self.board[i - 1][j - 1][0]:
                self.board[i - 1][j - 1][1] = True
            else:
                if not self.board[i - 1][j - 1][1]:
                    self.empty_cells(i - 1, j - 1)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

        elif 0 < i < self.height - 1 and not j:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i + 1][j + 1][0]:
                self.board[i + 1][j + 1][1] = True
            else:
                if not self.board[i + 1][j + 1][1]:
                    self.empty_cells(i + 1, j + 1)

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i - 1][j + 1][0]:
                self.board[i - 1][j + 1][1] = True
            else:
                if not self.board[i - 1][j + 1][1]:
                    self.empty_cells(i - 1, j + 1)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

        elif 0 < i < self.height - 1 and j == self.width - 1:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i + 1][j - 1][0]:
                self.board[i + 1][j - 1][1] = True
            else:
                if not self.board[i + 1][j - 1][1]:
                    self.empty_cells(i + 1, j - 1)

            if self.board[i - 1][j - 1][0]:
                self.board[i - 1][j - 1][1] = True
            else:
                if not self.board[i - 1][j - 1][1]:
                    self.empty_cells(i - 1, j - 1)

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

        else:

            if self.board[i + 1][j][0]:
                self.board[i + 1][j][1] = True
            else:
                if not self.board[i + 1][j][1]:
                    self.empty_cells(i + 1, j)

            if self.board[i + 1][j + 1][0]:
                self.board[i + 1][j + 1][1] = True
            else:
                if not self.board[i + 1][j + 1][1]:
                    self.empty_cells(i + 1, j + 1)

            if self.board[i + 1][j - 1][0]:
                self.board[i + 1][j - 1][1] = True
            else:
                if not self.board[i + 1][j - 1][1]:
                    self.empty_cells(i + 1, j - 1)

            if self.board[i][j - 1][0]:
                self.board[i][j - 1][1] = True
            else:
                if not self.board[i][j - 1][1]:
                    self.empty_cells(i, j - 1)

            if self.board[i][j + 1][0]:
                self.board[i][j + 1][1] = True
            else:
                if not self.board[i][j + 1][1]:
                    self.empty_cells(i, j + 1)

            if self.board[i - 1][j][0]:
                self.board[i - 1][j][1] = True
            else:
                if not self.board[i - 1][j][1]:
                    self.empty_cells(i - 1, j)

            if self.board[i - 1][j + 1][0]:
                self.board[i - 1][j + 1][1] = True
            else:
                if not self.board[i - 1][j + 1][1]:
                    self.empty_cells(i - 1, j + 1)

            if self.board[i - 1][j - 1][0]:
                self.board[i - 1][j - 1][1] = True
            else:
                if not self.board[i - 1][j - 1][1]:
                    self.empty_cells(i - 1, j - 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 300, 450
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    # формирование кадра:
    # команды рисования на холсте
    pygame.display.set_caption('Папа сапёра')

    board = Minesweeper(10, 15, 10)
    board.set_view(0, 0, 30)
    running = True
    flag = False
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                board.render(screen)
        board.render(screen)
        # обновление экрана
        pygame.display.flip()
    # завершение работы:
    pygame.quit()
