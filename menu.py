import pygame
import time
import pygame_gui
import sys

class Menu:
    def __init__(self,m):
        self.settings = m.settings
        self.screen = m.screen

    def create_buttons(self):
        center_x = self.settings.screen_width // 2
        y = self.settings.screen_height//4
        width_all = 0.7*self.settings.screen_width
        height = 0.1*self.settings.screen_height
        gap_h = 0.1*height
        gap_w = 0.05*width_all
        width = 0.3*width_all
        self.button_all_paths_rect = pygame.Rect(center_x - width_all//2, 
                                                 y, width_all, height)
        self.button_simple_dijkstra_rect = pygame.Rect(center_x - 1.5*width - gap_w, 
                                                       y + height + gap_h, width, height)
        self.button_dijkstra_rect = pygame.Rect(center_x - 0.5*width, y + height + gap_h,
                                                width, height)
        self.button_astar_rect = pygame.Rect(center_x + 0.5*width + gap_w, 
                                             y + height + gap_h, width, height)
        self.button_all_rect = pygame.Rect(center_x - width_all//2,y + 2*height + 2*gap_h, 
                                           width_all, height)
        self.new_maze_rect = pygame.Rect(center_x - width_all//2, y + 3*height + 3*gap_h, 
                                           width_all, height)
        font = pygame.font.SysFont(self.settings.font, 20, bold=True)
        self.button_all_paths_text = font.render("find all paths", True, 
                                                       self.settings.font_color) 
        self.button_simple_dijkstra_text = font.render("simple_dijkstra", True, 
                                                       self.settings.font_color) 
        self.button_dijkstra_text = font.render("dijkstra", True, self.settings.font_color)  
        self.button_astar_text = font.render("astar", True, self.settings.font_color)  
        self.button_all_text = font.render("all", True, self.settings.font_color) 
        self.new_maze_text = font.render("new maze", True, self.settings.font_color) 
    
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
        pygame.draw.rect(self.screen, self.settings.button_color, self.new_maze_rect) 
        self.screen.blit(self.new_maze_text, 
                         (self.new_maze_rect.centerx - self.new_maze_text.get_width() // 2,
                          self.new_maze_rect.centery - self.new_maze_text.get_height() // 2)) 
         
        pygame.display.update()

    def set_maze_size(self):
        pygame.font.SysFont(self.settings.font, 20, bold=True)
        self.manager = pygame_gui.UIManager((self.settings.screen_width, 
                                               self.settings.screen_height))
        self.width_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.settings.screen_width/1.7, self.settings.screen_height/3), (self.settings.screen_width/4, self.settings.screen_height/20)), manager=self.manager,object_id='#w')
        self.height_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.settings.screen_width/1.7, self.settings.screen_height-self.settings.screen_height/3), (self.settings.screen_width/4, self.settings.screen_height/20)), manager=self.manager,object_id='#h')
        font = pygame.font.SysFont(self.settings.font, 20, bold=True)
        width = font.render('Input maze width (5-500, Enter)', True, self.settings.font_color)
        height = font.render('Input maze height (5-500, Enter)', True, self.settings.font_color)
        widthRect = width.get_rect(topleft=(self.settings.screen_width/8, self.settings.screen_height/3+5))
        heightRect = height.get_rect(topleft=(self.settings.screen_width/8, self.settings.screen_height-self.settings.screen_height/3+5))
        
        self.clock = pygame.time.Clock()
        size = {}
        while True:
            UI_REFRESH_RATE = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#w'):
                    size["width"] = int(event.text)
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#h'):
                    size["height"] = int(event.text)                
                self.manager.process_events(event)
            if len(size) ==2 and size["width"] in range(5,501) and size["height"] in range(5,501):
                break
            self.manager.update(UI_REFRESH_RATE)
            self.screen.fill("white")
            self.screen.blit(width, widthRect)
            self.screen.blit(height, heightRect)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.settings.maze_width = size["width"]
        self.settings.maze_height = size["height"]
        self.settings.check_maze_size()
        self.settings.create_screen()
        self.settings.cell_width = self.settings.screen_width/self.settings.maze_width
        self.settings.cell_height = self.settings.screen_height/self.settings.maze_height
        self.settings.solve_time = 0.01*11/self.settings.maze_width
        self.settings.shortest_path_time = 0.04*11/self.settings.maze_width
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                               self.settings.screen_height))
        pygame.display.update()
    