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
        self.speed_paths = {}

    def find_fastest(self):
        prev_prev_cell = []
        prev_cell = []
        for path in self.paths:
            speed = self.settings.corner_speed
            all_speeds = 0
            path = eval(path)
            for cell in path:
                all_speeds +=speed
                if cell[1] == 0:
                    speed += self.settings.acceleration
                    prev_cell = [cell[0],cell[1]]
                    continue
                if cell[1] == 1:
                    speed += self.settings.acceleration
                    prev_prev_cell = [prev_cell[0], prev_cell[1]]
                    prev_cell = [cell[0],cell[1]]
                    continue
                if cell[0] != prev_prev_cell[0] and cell[1] != prev_prev_cell[1]:
                    speed = self.settings.corner_speed
                else:
                    speed += self.settings.acceleration
                prev_prev_cell = [prev_cell[0], prev_cell[1]]
                prev_cell = [cell[0],cell[1]]
            self.speed_paths[str(path)] = all_speeds/self.paths[str(path)]

                
    async def draw_fastest(self):
        for path in self.speed_paths:
            path=eval(path)
            for cell in path:
                pygame.draw.rect(self.screen, self.settings.shortest_path_color, 
                             (cell[1]*self.settings.cell_width, cell[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))              
                time.sleep(0.01)
                pygame.display.update()
                await asyncio.sleep(0)
            time.sleep(0.4)
            await asyncio.sleep(0)
            break
                
    async def fastest(self, finish):
        self.finish = finish
        self.paths = await self.all_paths.make_paths(self.finish)
        self.find_fastest()
        self.speed_paths = dict(sorted(self.speed_paths.items(), key=lambda item: item[1]))
        await self.draw_fastest()
        time.sleep(1)