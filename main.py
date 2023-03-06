import pygame
import sys
from settings import Settings
from maze import Maze
from simplified_dijkstra import SimpleDijkstra
from dijkstra import Dijkstra
from astar import Astar
from all_paths import AllPaths
import time

class Main:
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                               self.settings.screen_height))
        self.grid = [[0 for i in range(self.settings.maze_width)] 
                     for j in range(self.settings.maze_height)]
        self.maze = Maze(self)
        self.simple_dijkstra = SimpleDijkstra(self)
        self.dijkstra = Dijkstra(self)
        self.astar = Astar(self)
        self.all_paths = AllPaths(self)

    def create_buttons(self):
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2       
        width_all = 0.7*self.settings.screen_width
        height = 0.1*self.settings.screen_height
        gap_h = 0.1*height
        gap_w = 0.05*width_all
        width = 0.3*width_all
        self.button_all_paths_rect = pygame.Rect(center_x - width_all//2, 
                                                 center_y  - 1.5*height - gap_h, width_all, height)
        self.button_simple_dijkstra_rect = pygame.Rect(center_x - 1.5*width - gap_w, 
                                                       center_y - height//2, width, height)
        self.button_dijkstra_rect = pygame.Rect(center_x - 0.5*width, center_y - height//2,
                                                width, height)
        self.button_astar_rect = pygame.Rect(center_x + 0.5*width + gap_w, 
                                             center_y - height//2, width, height)
        self.button_all_rect = pygame.Rect(center_x - width_all//2, center_y  + gap_h + height//2, 
                                           width_all, height)
        font = pygame.font.SysFont(self.settings.font, 20, bold=True)
        self.button_all_paths_text = font.render("find all paths", True, 
                                                       self.settings.font_color) 
        self.button_simple_dijkstra_text = font.render("simple_dijkstra", True, 
                                                       self.settings.font_color) 
        self.button_dijkstra_text = font.render("dijkstra", True, self.settings.font_color)  
        self.button_astar_text = font.render("astar", True, self.settings.font_color)  
        self.button_all_text = font.render("all", True, self.settings.font_color) 
    
    def draw_buttons(self):
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_all_paths_rect)
        self.screen.blit(self.button_all_paths_text, 
                         (self.button_all_paths_rect.centerx 
                          - self.button_all_paths_text.get_width() // 2, 
                          self.button_all_paths_rect.centery 
                          - self.button_all_paths_text.get_height() // 2))
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_simple_dijkstra_rect)
        self.screen.blit(self.button_simple_dijkstra_text, 
                         (self.button_simple_dijkstra_rect.centerx 
                          - self.button_simple_dijkstra_text.get_width() // 2, 
                          self.button_simple_dijkstra_rect.centery 
                          - self.button_simple_dijkstra_text.get_height() // 2))
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_dijkstra_rect)
        self.screen.blit(self.button_dijkstra_text, 
                         (self.button_dijkstra_rect.centerx 
                          - self.button_dijkstra_text.get_width() // 2,  
                          self.button_dijkstra_rect.centery 
                          - self.button_dijkstra_text.get_height() // 2))
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_astar_rect)
        self.screen.blit(self.button_astar_text, 
                         (self.button_astar_rect.centerx - self.button_astar_text.get_width() // 2,
                          self.button_astar_rect.centery 
                          - self.button_astar_text.get_height() // 2)) 
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_all_rect)  
        self.screen.blit(self.button_all_text, 
                         (self.button_all_rect.centerx - self.button_all_text.get_width() // 2,
                          self.button_all_rect.centery - self.button_all_text.get_height() // 2)) 
        pygame.display.update()

    def main(self):
        self.maze.create_maze()
        self.create_buttons()
        while True:
            self.draw_buttons()
            algorithm = ""
            flag =1 
            while flag:           
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_all_paths_rect.collidepoint(event.pos):
                            algorithm = "all_paths"
                            flag =0
                            break
                        elif self.button_simple_dijkstra_rect.collidepoint(event.pos):
                            algorithm = "simple_dijkstra"
                            flag =0
                            break
                        elif self.button_dijkstra_rect.collidepoint(event.pos):
                            algorithm = "dijkstra"
                            flag =0
                            break
                        elif self.button_astar_rect.collidepoint(event.pos):
                            algorithm = "astar"
                            flag =0
                            break
                        elif self.button_all_rect.collidepoint(event.pos):
                            algorithm = "all"
                            flag =0
                            break
            self.maze.draw_maze()
            time.sleep(1)
            if algorithm == "all_paths":
                self.all_paths.solve_maze(self.maze.finish)
                # print all paths
                # for key, value in self.all_paths.paths.items():
                #     print(key, ' : ', value)
            elif algorithm == "simple_dijkstra":
                self.simple_dijkstra.solve_maze(self.maze.finish)
            elif algorithm == "dijkstra":          
                self.dijkstra.solve_maze(self.maze.finish)          
            elif algorithm == "astar":
                self.astar.solve_maze(self.maze.finish)
            elif algorithm == "all":
                start_time = time.time()
                self.simple_dijkstra.solve_maze(self.maze.finish)
                end_time = time.time()
                print("Simplified Dijkstra algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
                self.maze.draw_maze()
                start_time = time.time()
                self.dijkstra.solve_maze(self.maze.finish)
                end_time = time.time()
                print("Dijkstra algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
                self.maze.draw_maze()
                start_time = time.time()
                self.astar.solve_maze(self.maze.finish)
                end_time = time.time()
                print("A* algorithm took", end_time - start_time, "seconds")
                time.sleep(0.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    game = Main()
    game.main()