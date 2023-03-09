import pygame
import random
import time
import asyncio

class Maze:
    def __init__(self, m):       
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.frontiers = []
        self.visited = []
        self.finish = (1,1)
            
    def add_frontiers(self, i,j):
        if i>1 and self.grid[i-2][j]==0:
            self.frontiers.append((i-2,j, i-1,j))
        if i<self.settings.maze_height-2 and self.grid[i+2][j]==0:
            self.frontiers.append((i+2,j, i+1, j))
        if j>1 and self.grid[i][j-2]==0:
            self.frontiers.append((i,j-2, i , j-1))
        if j<self.settings.maze_width-2 and self.grid[i][j+2]==0:
            self.frontiers.append((i,j+2, i, j+1))

    def set_finish(self):
        for i in range(self.settings.maze_height -1 , -1,-1):
            if self.grid[i][self.settings.maze_width-2]==1:
                return (i,self.settings.maze_width-1)
            
    async def create_grid(self):
        self.grid[self.settings.first[0]][self.settings.first[1]] = 1
        self.grid[self.settings.start[0]][self.settings.start[1]] = 1
        pygame.draw.rect(self.screen, self.settings.start_color, 
                         (self.settings.start[1]*self.settings.cell_width, 
                          self.settings.start[0]*self.settings.cell_height, 
                          self.settings.cell_width, self.settings.cell_height))
        pygame.display.update()
        pygame.draw.rect(self.screen, self.settings.color, 
                         (self.settings.first[1]*self.settings.cell_width, 
                          self.settings.first[0]*self.settings.cell_height, 
                          self.settings.cell_width, self.settings.cell_height))
        pygame.display.update()
        self.add_frontiers(self.settings.first[0],self.settings.first[1])
        while len(self.frontiers)>0:
            next = random.choice(self.frontiers)
            if self.grid[next[0]][next[1]] == 1:
                self.frontiers.remove(next)
                continue
            self.grid[next[0]][next[1]] = 1
            pygame.draw.rect(self.screen, self.settings.color, 
                             (next[1]*self.settings.cell_width, next[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            self.grid[next[2]][next[3]] = 1
            pygame.draw.rect(self.screen, self.settings.color, 
                             (next[3]*self.settings.cell_width, next[2]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            self.frontiers.remove(next)
            self.add_frontiers(next[0],next[1])
            time.sleep(self.settings.solve_time)
            await asyncio.sleep(0)
        self.finish = self.set_finish()
        self.grid[self.finish[0]][self.finish[1]] = 1
        self.add_connections()
        pygame.draw.rect(self.screen, self.settings.finish_color, 
                         (self.finish[1]*self.settings.cell_width, 
                          self.finish[0]*self.settings.cell_height, self.settings.cell_width, 
                          self.settings.cell_height))
        pygame.display.update()
        await asyncio.sleep(0)

    def check_valid_connection(self, row, col):
        if (self.grid[row-1][ col] ==1 and self.grid[row+1][ col] ==1 
            and self.grid[row][ col-1]==0 and self.grid[row][ col+1]==0):
            return True
        if (self.grid[row-1][col] ==0 and self.grid[row+1][col] ==0 
            and self.grid[row][col-1]==1 and self.grid[row][col+1]==1):
            return True
        return False

    def add_connections(self):
        max_number = int((self.settings.maze_width + self.settings.maze_height)/6)
        number = 0
        possibilites = []
        for row, l in enumerate(self.grid[1:self.settings.maze_height-1],1):
            for col, value in enumerate(l[1:self.settings.maze_width-1],1):
                if value == 0:
                    possibilites.append((row,col))
        while number!=max_number:
            tup = random.choice(possibilites)      
            if self.check_valid_connection(tup[0],tup[1]):
                possibilites.remove(tup)
                self.grid[tup[0]][tup[1]] =1
                number+=1
                pygame.draw.rect(self.screen, self.settings.color, 
                                 (tup[1]*self.settings.cell_width, 
                                  tup[0]*self.settings.cell_height, self.settings.cell_width, 
                                  self.settings.cell_height))
                pygame.display.update()
    
    def draw_maze(self):
        black = (0,0,0)
        for row, l in enumerate(self.grid):
            for col, value in enumerate(l):
                if value == 1:
                    pygame.draw.rect(self.screen, self.settings.color, 
                                     (col*self.settings.cell_width, row*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                else:
                    pygame.draw.rect(self.screen, black, 
                                     (col*self.settings.cell_width, row*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
        pygame.draw.rect(self.screen, self.settings.start_color, 
                         (self.settings.start[1]*self.settings.cell_width, 
                          self.settings.start[0]*self.settings.cell_height, 
                          self.settings.cell_width, self.settings.cell_height))
        pygame.draw.rect(self.screen, self.settings.start_color, 
                         (self.finish[1]*self.settings.cell_width, 
                          self.finish[0]*self.settings.cell_height, self.settings.cell_width, 
                          self.settings.cell_height))
        pygame.display.update()

    async def create_maze(self):
        await self.create_grid()
