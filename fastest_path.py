import pygame
import time
import asyncio
from all_paths import AllPaths

class Fastest:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.finish = m.maze.finish
        self.maze = m.maze
        self.all_paths = AllPaths(m)
        self.fastest_path = []

    def find_fastest(self):
        prev_prev_cell = []
        prev_cell = []
        #maze always start in the same place so I know that first and second field can't be a corner so I use it to mark first and second field as prev_prev and prev
        i = 0
        lowest_path_time = 1e100
        for path in self.paths:
            speed = self.settings.start_speed
            #time it takes to go through the path
            path_time = 0          
            path = eval(path)
            for cell in path:
                #first field
                if i == 0:
                    speed += self.settings.acceleration
                    prev_cell = [cell[0],cell[1]]
                    path_time +=1/speed
                    i+=1
                    continue
                #second field
                if i == 1:
                    speed += self.settings.acceleration
                    prev_prev_cell = [prev_cell[0], prev_cell[1]]
                    prev_cell = [cell[0],cell[1]]
                    path_time +=1/speed
                    i+=1
                    continue
                if cell[0] != prev_prev_cell[0] and cell[1] != prev_prev_cell[1]:
                    speed = self.settings.corner_speed
                else:
                    speed += self.settings.acceleration
                prev_prev_cell = [prev_cell[0], prev_cell[1]]
                prev_cell = [cell[0],cell[1]]
                path_time +=1/speed
            if path_time < lowest_path_time:
                lowest_path_time = path_time
                self.fastest_path = path

    async def draw_fastest(self):
        for cell in self.fastest_path:
            pygame.draw.rect(self.screen, self.settings.fastest_path_color, 
                             (cell[1]*self.settings.cell_width, cell[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))              
            time.sleep(0.01)
            pygame.display.update()
            await asyncio.sleep(0)
        time.sleep(0.4)
        await asyncio.sleep(0)
                
    async def fastest(self, finish):
        self.finish = finish
        self.paths = await self.all_paths.make_paths(self.finish)
        self.find_fastest()
        await self.draw_fastest()
        time.sleep(1)