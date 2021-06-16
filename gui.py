import sys
from typing import Union

import pygame
import requests

pygame.init()
pygame.font.init()


def findEmpty(board: list[list[int]]) -> Union[tuple[int, int], tuple[None, None]]:
    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                return row, col
    return None, None


def isValid(board: list[list[int]], guess: int, row: int, col: int) -> bool:
    row_values = board[row]
    col_values = [board[i][col] for i in range(9)]
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    if guess in row_values or guess in col_values:
        return False

    for row in range(row_start, row_start + 3):
        for col in range(col_start, col_start + 3):
            if board[row][col] == guess:
                return False

    return True


def GetBoard():
    return requests.get("https://sugoku.herokuapp.com/board?difficulty=random").json()["board"]


class Sudoku:
    screenSize = (WIDTH, HEIGHT) = (450, 500)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SUDOKU")

    g = GetBoard()

    running = True

    font1 = pygame.font.SysFont("comicsans", 40)
    font2 = pygame.font.SysFont("impact", 20)

    dif = WIDTH // 9

    x, y = 1, 1

    isSolving = False

    def GetCoord(self, mouse_pos: tuple[int, int]):
        return mouse_pos[0] // self.dif, mouse_pos[1] // self.dif

    def HighlightSquare(self, coord):
        pygame.draw.line(self.screen, (200, 150, 200),
                         (self.dif * coord[0], self.dif * coord[1]),
                         (self.dif * coord[0] + self.dif, self.dif * coord[1]), 7)
        pygame.draw.line(self.screen, (200, 150, 200),
                         (self.dif * coord[0], self.dif * coord[1]),
                         (self.dif * coord[0], self.dif * coord[1] + self.dif), 7)
        pygame.draw.line(self.screen, (200, 150, 200),
                         (self.dif * coord[0], self.dif * coord[1] + self.dif),
                         (self.dif * coord[0] + self.dif, self.dif * coord[1] + self.dif), 7)
        pygame.draw.line(self.screen, (200, 150, 200),
                         (self.dif * coord[0] + self.dif, self.dif * coord[1]),
                         (self.dif * coord[0] + self.dif, self.dif * coord[1] + self.dif), 7)

    def DrawGrid(self, grid):
        for i in range(9):
            for j in range(9):
                if self.g[i][j] != 0:
                    text1 = self.font1.render(str(grid[i][j]), True, (255, 255, 255))
                    self.screen.blit(text1, (i * self.dif + 19, j * self.dif + 14))

        for i in range(10):
            if i % 3 == 0:
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, 'white', (0, i * self.dif),
                             (self.WIDTH, i * self.dif), thick)
            pygame.draw.line(self.screen, 'white', (i * self.dif, 0),
                             (i * self.dif, self.WIDTH), thick)

    def Reset(self):
        self.g = [[0 for _ in range(9)] for _ in range(9)]

    def Solve(self):
        row, col = findEmpty(self.g)
        if row is None:
            return self.g

        for i in range(1, 10):
            if isValid(self.g, i, row, col):
                self.g[row][col] = i
                if self.Solve():
                    return self.g
            self.g[row][col] = 0

        return False

    def Instructions(self):
        text1 = self.font2.render(
            "PRESS R TO EMPTY", True, (255, 255, 255))
        text2 = self.font2.render(
            "ENTER VALUES AND PRESS S TO SOLVE", True, (255, 255, 255))
        self.screen.blit(text1, (20, 455))
        self.screen.blit(text2, (20, 475))

    def Draw(self):
        self.DrawGrid(self.g)
        self.HighlightSquare((self.x, self.y))
        self.Instructions()

    def __init__(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.x, self.y = self.GetCoord(pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x -= 1
                    if event.key == pygame.K_RIGHT:
                        self.x += 1
                    if event.key == pygame.K_UP:
                        self.y -= 1
                    if event.key == pygame.K_DOWN:
                        self.y += 1
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        if isValid(self.g, 1, self.x, self.y):
                            self.g[self.x][self.y] = 1
                    if event.key in [pygame.K_2, pygame.K_KP2]:
                        if isValid(self.g, 2, self.x, self.y):
                            self.g[self.x][self.y] = 2
                    if event.key in [pygame.K_3, pygame.K_KP3]:
                        if isValid(self.g, 3, self.x, self.y):
                            self.g[self.x][self.y] = 3
                    if event.key in [pygame.K_4, pygame.K_KP4]:
                        if isValid(self.g, 4, self.x, self.y):
                            self.g[self.x][self.y] = 4
                    if event.key in [pygame.K_5, pygame.K_KP5]:
                        if isValid(self.g, 5, self.x, self.y):
                            self.g[self.x][self.y] = 5
                    if event.key in [pygame.K_6, pygame.K_KP6]:
                        if isValid(self.g, 6, self.x, self.y):
                            self.g[self.x][self.y] = 6
                    if event.key in [pygame.K_7, pygame.K_KP7]:
                        if isValid(self.g, 7, self.x, self.y):
                            self.g[self.x][self.y] = 7
                    if event.key in [pygame.K_8, pygame.K_KP8]:
                        if isValid(self.g, 8, self.x, self.y):
                            self.g[self.x][self.y] = 8
                    if event.key in [pygame.K_9, pygame.K_KP9]:
                        if isValid(self.g, 9, self.x, self.y):
                            self.g[self.x][self.y] = 9

                    if event.key == pygame.K_s:
                        self.isSolving = True

                    if event.key == pygame.K_r:
                        self.Reset()

                    if event.key == pygame.K_f:
                        self.g = GetBoard()

            self.x = min(max(0, self.x), 8)
            self.y = min(max(0, self.y), 8)
            self.screen.fill((28, 30, 31))
            if not self.isSolving:
                self.Draw()
            else:
                self.isSolving = not self.Solve()
            pygame.display.flip()


if __name__ == '__main__':
    sudoku = Sudoku()
