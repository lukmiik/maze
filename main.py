import asyncio
import pygame
import sys
import pygame_gui
from settings import Settings
from maze import Maze
from simplified_dijkstra import SimpleDijkstra
from dijkstra import Dijkstra
from astar import Astar
from all_paths import AllPaths
from fastest_path import Fastest
from menu import Menu
import time

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Maze')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                               self.settings.screen_height))
        self.menu = Menu(self)

    async def main(self):        
        await self.menu.set_maze_size()
        self.grid = [[0 for i in range(self.settings.maze_width)] 
                     for j in range(self.settings.maze_height)]
        self.maze = Maze(self)
        self.simple_dijkstra = SimpleDijkstra(self)
        self.dijkstra = Dijkstra(self)
        self.astar = Astar(self)
        self.all_paths = AllPaths(self)
        self.fastest_path = Fastest(self)
        await self.maze.create_maze()
        self.menu.create_buttons()
        time.sleep(0.5)
        while True:
            self.menu.draw_buttons()
            algorithm = ""
            flag =1 
            while flag:           
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.button_all_paths_rect.collidepoint(event.pos):
                            algorithm = "all_paths"
                            flag =0
                            break
                        elif self.menu.button_simple_dijkstra_rect.collidepoint(event.pos):
                            algorithm = "simple_dijkstra"
                            flag =0
                            break
                        elif self.menu.button_dijkstra_rect.collidepoint(event.pos):
                            algorithm = "dijkstra"
                            flag =0
                            break
                        elif self.menu.button_astar_rect.collidepoint(event.pos):
                            algorithm = "astar"
                            flag =0
                            break
                        elif self.menu.button_all_rect.collidepoint(event.pos):
                            algorithm = "all"
                            flag =0
                            break  
                        elif self.menu.new_maze_rect.collidepoint(event.pos):
                            algorithm = "new"
                            flag =0
                            break  
                        elif self.menu.fastest_rect.collidepoint(event.pos):
                            algorithm = "fastest"
                            flag =0
                            break  
                pygame.display.update()
                await asyncio.sleep(0)
            time.sleep(0.2)
            self.maze.draw_maze()
            if algorithm == "all_paths":
                await self.all_paths.solve_maze(self.maze.finish)
            elif algorithm == "simple_dijkstra":
                await self.simple_dijkstra.solve_maze(self.maze.finish)
            elif algorithm == "dijkstra":          
                await self.dijkstra.solve_maze(self.maze.finish)          
            elif algorithm == "astar":
                await self.astar.solve_maze(self.maze.finish)
            elif algorithm == "all":
                start_time = time.time()
                await self.simple_dijkstra.solve_maze(self.maze.finish)
                end_time = time.time()
                print("Simplified Dijkstra algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
                self.maze.draw_maze()
                start_time = time.time()
                await self.dijkstra.solve_maze(self.maze.finish)
                end_time = time.time()
                print("Dijkstra algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
                self.maze.draw_maze()
                start_time = time.time()
                await self.astar.solve_maze(self.maze.finish)
                end_time = time.time()
                print("A* algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
            elif algorithm == "fastest":
                await self.fastest_path.fastest(self.maze.finish)
            elif algorithm == "new":
                game = Main()
                await game.main()
            pygame.display.update()
            await asyncio.sleep(0)

if __name__ == '__main__':
    game = Main()
    asyncio.run(game.main())