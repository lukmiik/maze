import pygame
import time
import copy
import asyncio

class AllPaths:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.finish = m.maze.finish
        self.maze = m.maze
        self.paths = {}

    def find_pahts(self, row,col, path, count):
        time.sleep(0)
        if self.grid[row][col+1] == 1 and (row,col+1) not in path:
            temp = copy.deepcopy(path)
            temp.append((row,col+1))
            if (row,col+1) == self.finish:
                self.paths[str(temp)] = count+1
                return
            self.find_pahts(row, col+1, temp, count+1)
        if self.grid[row+1][col] == 1 and (row+1,col) not in path:
            temp = copy.deepcopy(path)
            temp.append((row+1,col))
            if (row+1,col) == self.finish:
                self.paths[str(temp)] = count+1
                return
            self.find_pahts(row+1, col, temp, count+1)
        if self.grid[row][col-1] == 1 and (row,col-1) not in path:
            temp = copy.deepcopy(path)
            temp.append((row,col-1))
            if (row,col-1) == self.finish:
                self.paths[str(temp)] = count+1
                return
            self.find_pahts(row, col-1, temp, count+1)
        if self.grid[row-1][col] == 1 and (row-1,col) not in path:
            temp = copy.deepcopy(path)
            temp.append((row-1,col))
            if (row-1,col) == self.finish:
                self.paths[str(temp)] = count+1
                return
            self.find_pahts(row-1, col, temp, count+1)

    async def draw_paths(self):
        for path in self.paths:
            path = eval(path)
            for cell in path:
                pygame.draw.rect(self.screen, self.settings.shortest_path_color, 
                             (cell[1]*self.settings.cell_width, cell[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))              
                time.sleep(0.01)
                pygame.display.update()
                await asyncio.sleep(0)
            time.sleep(0.4)
            await asyncio.sleep(0)
            self.maze.draw_maze()
    
    async def make_paths(self,finish):
        self.finish = finish
        self.find_pahts(self.settings.start[0], self.settings.start[1],[self.settings.start],0)
        await self.draw_paths()
        return self.paths

    async def solve_maze(self, finish):
        self.finish = finish
        st= time.time()
        self.find_pahts(self.settings.start[0], self.settings.start[1],[self.settings.start],0)
        et = time.time()
        print("time to find all paths ", et-st, "seconds")
        self.paths = dict(sorted(self.paths.items(), key=lambda item: item[1]))
        await self.draw_paths()
