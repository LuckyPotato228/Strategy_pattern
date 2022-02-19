import sys
import pygame
from abc import ABC, abstractmethod
CONSOLE = 0
FILE = 1
PYGAME = 2


def get_data():
    data = [0] * 5
    for i in range(len(data)):
        data[i] = [i * j for j in range(10)]
    data[0][0] = ''
    return data


def get_format_str(width=5):
    return '{:^' + str(width) + '}'

class Drawer(ABC):

    @abstractmethod
    def drawing(self, data):
        pass

class Context:
    def __init__(self, strategy: Drawer)-> None:
        self._strategy = strategy
    @property
    def strategy(self) -> Drawer:
        return self._strategy
    @strategy.setter
    def strategy(self, strategy: Drawer) -> None:
        self._strategy = strategy

    def draw(self) -> None:
        result = self._strategy.drawing()


class FileDrawer(Drawer):
    def __init__(self, width, filename):
        self.width = width
        self.filename = filename

    def draw(self, data):
        rows = len(data)
        cols = len(data[0])
        result = [
            '##' + '=' * self.width + '##' + ('=' * self.width + '#') * cols + '#',
            '||' + ' ' * self.width + '||' + ''.join(
                [(get_format_str(self.width) + '|').format(i) for i in range(len(data[0]))]) + '|',
            '##' + '=' * self.width + '##' + ('=' * self.width + '#') * cols + '#',
        ]
        for i in range(rows):
            row = data[i]
            f = '||' + get_format_str(self.width) + '||'
            s = f.format(i)
            for item in row:
                s += get_format_str(self.width).format(item)
                s += '|'
            result.append(s + '|')
        result.append('##' + '=' * self.width + '##' + ('=' * self.width + '#') * cols + '#', )
        f = open('output.txt', 'w')
        f.write('\n'.join(result))
        f.close()


class PGDrawer(Drawer):
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Инициализация модуля font
        self.font = pygame.font.SysFont('Comic Sans MS', 20, True)
        self.screen = pygame.display.set_mode((800, 600))
        self.gameover = False

    @staticmethod
    def pg_draw_item(x, y, width, height, value, screen, font):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 0)
        data = str(value)
        ts = font.render(data, False, (0, 0, 0))
        text_width = ts.get_rect().width
        text_height = ts.get_rect().height
        screen.blit(ts, (x + (width - text_width) // 2, y + (height - text_height) // 2))

    def draw(self, data):
        while not self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
            width = 55
            height = 40
            space = 10
            self.screen.fill((80, 80, 80))
            for i in range(len(data)):
                row = data[i]
                for j in range(len(row)):
                    PGDrawer.pg_draw_item((width + space) * (i + 1),
                                          (height + space) * (j + 1),
                                          width, height, data[i][j], self.screen, self.font)
            pygame.display.flip()
            pygame.time.wait(10)


def draw(data, mode):
    if mode == CONSOLE:
        width = 5
        for row in data:
            for item in row:
                f = get_format_str(width)
                print(f.format(item), end=' ')
            print()
    elif mode == FILE:
        width = 5
        filename = 'output.txt'
        rows = len(data)
        cols = len(data[0])
        result = [
            '##' + '=' * width + '##' + ('=' * width + '#') * cols + '#',
            '||' + ' ' * width + '||' + ''.join(
                [(get_format_str(width) + '|').format(i) for i in range(len(data[0]))]) + '|',
            '##' + '=' * width + '##' + ('=' * width + '#') * cols + '#',
        ]
        for i in range(rows):
            row = data[i]
            f = '||' + get_format_str(width) + '||'
            s = f.format(i)
            for item in row:
                s += get_format_str(width).format(item)
                s += '|'
            result.append(s + '|')
        result.append('##' + '=' * width + '##' + ('=' * width + '#') * cols + '#', )
        f = open(filename, 'w')
        f.write('\n'.join(result))
        f.close()
    elif mode == PYGAME:
        d = PGDrawer()
        d.draw(data)



if __name__ == '__main__':
    print('Strategy unfinished example')
    print('0. Show two-dimensional array to console')
    print('1. Show two-dimensional array to file')
    context = Context(FileDrawer())
    context.draw()
    print()
    print('2. Show two-dimensional array to pygame window')
    mode = -1
    while mode < 0 or mode > 2:
        try:
            mode = int(input('Please, type in mode: '))
        except ValueError:
            mode = -1
    draw(get_data(), mode)
