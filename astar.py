import pygame
import time
from queue import PriorityQueue
import asyncio

class Astar:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.finish = m.maze.finish

    def heuristic(self, row, col):
        return abs(self.finish[0] - row) + abs(self.finish[1]-col)

    def add_neighbours(self, current):
        if (self.grid[current[0]-1][current[1]] == 1 
            and (current[0]-1,current[1]) not in self.visited):
            g_temp = self.g[current]+1
            if g_temp<self.g[current[0]-1,current[1]]:
                self.g[current[0]-1,current[1]] = self.g[current]+1
                self.f[current[0]-1,current[1]] =  self.g[current[0]-1,current[1]] 
                + self.heuristic(current[0]-1,current[1])
                self.p[current[0]-1,current[1]] = current
                self.pq.put((self.f[current[0]-1,current[1]], (current[0]-1,current[1])))
        if (self.grid[current[0]+1][current[1]] == 1 
            and (current[0]+1,current[1]) not in self.visited):
            g_temp = self.g[current]+1
            if g_temp<self.g[current[0]+1,current[1]]:
                self.g[current[0]+1,current[1]] = self.g[current]+1
                self.f[current[0]+1,current[1]] =  self.g[current[0]+1,current[1]] 
                + self.heuristic(current[0]+1,current[1])
                self.p[current[0]+1,current[1]] = current
                self.pq.put((self.f[current[0]+1,current[1]], (current[0]+1,current[1])))
        if (self.grid[current[0]][current[1]-1] == 1 
            and (current[0],current[1]-1) not in self.visited):
            g_temp = self.g[current]+1
            if g_temp<self.g[current[0],current[1]-1]:
                self.g[current[0],current[1]-1] = self.g[current]+1
                self.f[current[0],current[1]-1] =  self.g[current[0],current[1]-1] 
                + self.heuristic(current[0],current[1]-1)
                self.p[current[0],current[1]-1] = current
                self.pq.put((self.f[current[0],current[1]-1], (current[0],current[1]-1)))
        if (self.grid[current[0]][current[1]+1] == 1 
            and (current[0],current[1]+1) not in self.visited):
            g_temp = self.g[current]+1
            if g_temp<self.g[current[0],current[1]+1]:
                self.g[current[0],current[1]+1] = self.g[current]+1
                self.f[current[0],current[1]+1] =  self.g[current[0],current[1]+1] 
                + self.heuristic(current[0],current[1]+1)
                self.p[current[0],current[1]+1] = current
                self.pq.put((self.f[current[0],current[1]+1], (current[0],current[1]+1)))

    async def astar(self):
        self.pq = PriorityQueue()
        self.pq.put((0, self.settings.start))
        self.g = {}
        self.f = {}
        self.p = {}
        self.visited = []
        for row, l in enumerate(self.grid):
            for col, value in enumerate(l):
                if value == 1:
                    self.g[(row,col)] = float('inf')
                    self.f[(row,col)] = float('inf')
        self.g[self.settings.start] = 0
        self.f[self.settings.start] = 0
        while True:
            current = self.pq.get()[1]
            pygame.draw.rect(self.screen, self.settings.path_color, 
                             (current[1]*self.settings.cell_width, 
                              current[0]*self.settings.cell_height, 
                              self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            time.sleep(self.settings.solve_time)
            if current == self.finish:
                break
            self.visited.append(current)
            self.add_neighbours(current)
            await asyncio.sleep(0)

    def create_shortest_path(self):
        self.shortest_path = []
        node = self.finish
        self.shortest_path.insert(0, node)
        while self.p[node] != self.settings.start:
            self.shortest_path.insert(0, self.p[node])
            node = self.p[node]
        self.shortest_path.insert(0, self.p[node])

    async def draw_path(self):
        self.create_shortest_path()
        for i in self.shortest_path:
            pygame.draw.rect(self.screen, self.settings.astar_color, 
                             (i[1]*self.settings.cell_width, i[0]*self.settings.cell_height, 
                              self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            time.sleep(self.settings.shortest_path_time)
            await asyncio.sleep(0)

    async def solve_maze(self, finish):
        self.finish = finish
        await self.astar()
        await self.draw_path()
