import pygame
import time

class Dijkstra:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen
        self.grid = m.grid
        self.finish = m.maze.finish
        self.graph ={}

    def check_nei(self,row, col):
        if (self.grid[row-1][col] == 1 or self.grid[row+1][col] == 1) and (self.grid[row][col-1] == 1 or self.grid[row][col+1] == 1):
            return True
        return False

    def create_graph(self, row, col, dir):
        time.sleep(self.settings.solve_time)
        if dir != "N":       
            for i in range(row-1, 0, -1):
                if self.grid[i][col]==0:
                    break
                if (i,col) == self.finish:
                    self.graph[(row,col)][(i,col)]= row-i
                    self.graph[(i,col)]= {}
                    pygame.draw.rect(self.screen, self.settings.color, (col*self.settings.cell_width, i*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.draw.circle(self.screen, self.settings.finish_color, (col*self.settings.cell_width+self.settings.cell_width/2, i*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update() 
                    break    
                if self.check_nei(i, col):
                    self.graph[(row,col)][(i,col)]= row-i
                    self.graph[(i,col)]= {}
                    pygame.draw.circle(self.screen,  self.settings.finish_color, (col*self.settings.cell_width+self.settings.cell_width/2, i*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()            
                    self.create_graph(i,col, "S")
                    break
        if dir != "E":       
            for i in range(col+1, self.settings.maze_width):
                if self.grid[row][i]==0:
                    break
                if (row,i) == self.finish:
                    self.graph[(row,col)][(row,i)]= i-col
                    self.graph[(row,i)]= {}
                    pygame.draw.rect(self.screen, self.settings.color, (i*self.settings.cell_width, row*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.draw.circle(self.screen, self.settings.finish_color, (i*self.settings.cell_width+self.settings.cell_width/2,row*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()   
                    break   
                if self.check_nei(row, i):
                    self.graph[(row,col)][(row,i)]= i-col
                    self.graph[(row,i)]= {}
                    pygame.draw.circle(self.screen, self.settings.finish_color, (i*self.settings.cell_width+self.settings.cell_width/2,row*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()                
                    self.create_graph(row, i, "W")
                    break
        if dir != "S":       
            for i in range(row+1, self.settings.maze_height):
                if self.grid[i][col]==0:
                    break
                if (i,col) == self.finish:
                    self.graph[(row,col)][(i,col)]= i-row
                    self.graph[(i,col)]= {}
                    pygame.draw.rect(self.screen, self.settings.color, (col*self.settings.cell_width, i*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.draw.circle(self.screen, self.settings.finish_color, (col*self.settings.cell_width+self.settings.cell_width/2, i*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()
                    break  
                if self.check_nei(i, col):
                    self.graph[(row,col)][(i,col)]= i-row
                    self.graph[(i,col)]= {}
                    pygame.draw.circle(self.screen, self.settings.finish_color, (col*self.settings.cell_width+self.settings.cell_width/2, i*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()               
                    self.create_graph(i,col, "N")
                    break
        if dir != "W":       
            for i in range(col-1, 0,-1):
                if self.grid[row][i]==0:
                    break
                if (row,i) == self.finish:
                    self.graph[(row,col)][(row,i)]= col-i
                    self.graph[(row,i)]= {}
                    pygame.draw.rect(self.screen, self.settings.color, (i*self.settings.cell_width, row*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.draw.circle(self.screen, self.settings.finish_color, (i*self.settings.cell_width+self.settings.cell_width/2,row*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()   
                    break 
                if self.check_nei(row, i):
                    self.graph[(row,col)][(row,i)]= col-i
                    self.graph[(row,i)]= {}
                    pygame.draw.circle(self.screen, self.settings.finish_color, (i*self.settings.cell_width+self.settings.cell_width/2,row*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
                    pygame.display.update()                
                    self.create_graph(row, i, "E")
                    break
    
    def dijkstra(self):
        unvisited = []
        distance = {}
        
        self.parents = {}
        for i in self.graph:
            unvisited.append(i)     
            distance[i] = float('inf')
        distance[self.settings.start] = 0
        pygame.draw.rect(self.screen, self.settings.path_color, (self.settings.start[1]*self.settings.cell_width, self.settings.start[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
        pygame.display.update()
        x=1
        vertex = self.settings.start
        while x:
            for node in self.graph[vertex]:
                path = distance[vertex] + self.graph[vertex][node]
                if path < distance[node]:
                    distance[node] = path
                    self.parents[node] = vertex
                if node==self.finish:
                    pygame.draw.rect(self.screen, self.settings.path_color, (node[1]*self.settings.cell_width, node[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
                    pygame.display.update()
                    x=0
                    break
            if x ==0:
                break
            unvisited.remove(vertex)
            min = float('inf')
            for i in unvisited:
                if distance[i]<min:
                    min = distance[i]
                    vertex = i
            pygame.draw.rect(self.screen, self.settings.path_color, (vertex[1]*self.settings.cell_width, vertex[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
            pygame.display.update()
            time.sleep(self.settings.solve_time)
 
    def create_shortest_path(self):
        self.shortest_path = []
        node = self.finish
        self.shortest_path.insert(0, node)
        while self.parents[node] != self.settings.start:
            self.shortest_path.insert(0, self.parents[node])
            node = self.parents[node]
        self.shortest_path.insert(0, self.parents[node])

    def draw_shortest_path(self):
        for i in self.shortest_path[1:]:
            if self.parents[i][0] ==i[0]:         
                if self.parents[i][1] <i[1]:
                    pygame.draw.rect(self.screen, self.settings.shortest_path_color, (self.parents[i][1]*self.settings.cell_width, self.parents[i][0]*self.settings.cell_height, self.settings.cell_width*(i[1]-self.parents[i][1]+1), self.settings.cell_height))              
                else:
                    pygame.draw.rect(self.screen, self.settings.shortest_path_color, (i[1]*self.settings.cell_width, i[0]*self.settings.cell_height, self.settings.cell_width*(self.parents[i][1]-i[1]+1), self.settings.cell_height))
            else:
                if self.parents[i][0] < i[0]:
                    pygame.draw.rect(self.screen, self.settings.shortest_path_color, (self.parents[i][1]*self.settings.cell_width, self.parents[i][0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height*(i[0]-self.parents[i][0]+1)))
                else:
                    pygame.draw.rect(self.screen, self.settings.shortest_path_color, (i[1]*self.settings.cell_width, i[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height*(self.parents[i][0]-i[0]+1)))
            pygame.display.update()
            time.sleep(self.settings.shortest_path_time)


    def solve_maze(self,finish):
        self.finish = finish
        self.graph[self.settings.start]={}
        pygame.draw.rect(self.screen, self.settings.color, (self.settings.start[1]*self.settings.cell_width, self.settings.start[0]*self.settings.cell_height, self.settings.cell_width, self.settings.cell_height))
        pygame.draw.circle(self.screen, self.settings.finish_color, (self.settings.start[1]*self.settings.cell_width+self.settings.cell_width/2, self.settings.start[0]*self.settings.cell_height+self.settings.cell_height/2),  self.settings.cell_width/2)
        pygame.display.update() 
        self.create_graph(self.settings.start[0],self.settings.start[1],"W")
        self.dijkstra()
        self.create_shortest_path()
        self.draw_shortest_path()