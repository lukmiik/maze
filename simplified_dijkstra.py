import pygame
import time
import copy

class SimpleDijkstra:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.finish = m.maze.finish

    def check_neighbours(self,cell):
        temp = []
        if self.grid[cell[0]-1][cell[1]] == 1 and (cell[0]-1,cell[1]) not in self.visited:
            temp.append((cell[0]-1,cell[1]))
        if self.grid[cell[0]+1][cell[1]] == 1 and (cell[0]+1,cell[1]) not in self.visited:
            temp.append((cell[0]+1,cell[1]))
        if self.grid[cell[0]][cell[1]-1] == 1 and (cell[0],cell[1]-1) not in self.visited:
            temp.append((cell[0],cell[1]-1))
        if self.grid[cell[0]][cell[1]+1] == 1 and (cell[0],cell[1]+1) not in self.visited:
            temp.append((cell[0],cell[1]+1))
        return temp

    def find_path(self):
        self.shortest_path=[]
        for i in self.cells:
            if i['cell'] == self.finish:
                cell = i["cell"]
                path = i["path"]
                break
        while cell != self.settings.start:
            self.shortest_path.insert(0,cell)
            for i in self.cells:
                if i['cell'] == path:
                    cell = i["cell"]
                    if cell != self.settings.start:
                        path = i["path"]
                    break
        self.shortest_path.insert(0,cell)

    def draw_path(self):
        for i in self.shortest_path:
            pygame.draw.rect(self.screen, self.settings.shortest_path_color, 
                             (i[1]*self.settings.cell_width, i[0]*self.settings.cell_height, 
                              self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            time.sleep(self.settings.shortest_path_time)

    def simple_dijkstra(self):
        i=1
        last = [self.settings.start]
        self.visited = []
        self.cells = [{"cell":(1,0)}]
        while i:
            next_last = []
            for cell in last:
                temp = []
                if cell == self.finish:
                    pygame.draw.rect(self.screen, self.settings.path_color, 
                                     (cell[1]*self.settings.cell_width, 
                                      cell[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.display.update()
                    i=0
                    break
                pygame.draw.rect(self.screen,  self.settings.path_color, 
                                 (cell[1]*self.settings.cell_width, 
                                  cell[0]*self.settings.cell_height, 
                                  self.settings.cell_width, self.settings.cell_height))
                self.visited.append(cell)
                temp = self.check_neighbours(cell)
                next_last.extend(temp)
                for i in temp:
                    self.cells.append({"cell": i, "path": cell})
            pygame.display.update()
            last = copy.deepcopy(next_last)
            time.sleep(self.settings.solve_time)


    def solve_maze(self, finish):
        self.finish = finish
        self.simple_dijkstra()
        self.find_path()
        self.draw_path()