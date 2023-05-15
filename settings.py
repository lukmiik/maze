import pygame

class Settings:
    def __init__(self):
        self.maze_width = 10
        self.maze_height =10
        self.check_maze_size()
        self.start = (1,0)
        self.first = (1,1)
        self.shortest_path_color = (220,0,0)
        self.path_color = (0,34,255)
        self.start_color = (255, 0, 0)
        self.finish_color = (255, 0, 0)
        self.color = (255, 255, 255)
        self.fastest_path_color = (255,255,0)
        self.screen_width = 800
        self.screen_height = 800
        self.cell_width = self.screen_width/self.maze_width
        self.cell_height = self.screen_height/self.maze_height
        self.solve_time = 0.01
        self.shortest_path_time = 0.01
        pygame.font.init()
        self.font = 'Tahoma'
        self.font_color = (0,0,0)  
        self.button_color = (255,140,0)
        self.corner_speed = 1
        self.start_speed = 1
        self.acceleration = 1
        # self.button_image = pygame.image.load('menu_icon.png')
        # self.button_image = pygame.transform.scale(self.button_image, (int(self.cell_width), int(self.cell_height)))

    def create_screen(self):
        pygame.display.init()
        max_width = pygame.display.Info().current_w
        max_height= pygame.display.Info().current_h - 50
        if self.maze_width>self.maze_height:   
            x = self.maze_width/self.maze_height
            self.screen_height = 800//self.maze_height*self.maze_height
            self.screen_width = int((800*x)//self.maze_width*self.maze_width)
            if self.screen_width>max_width:
                self.screen_width = max_width//self.maze_width*self.maze_width
                self.screen_height = int((self.screen_width/x)//self.maze_height*self.maze_height)
        elif self.maze_width<self.maze_height:
            x = self.maze_height/self.maze_width
            self.screen_width = 800//self.maze_width*self.maze_width
            self.screen_height = int((800*x)//self.maze_height*self.maze_height)
            if self.screen_height>max_height:
                self.screen_height = max_height//self.maze_height*self.maze_height
                self.screen_width = int((self.screen_height/x)//self.maze_width*self.maze_width)
        else:
            self.screen_width = int((800+self.maze_width)//self.maze_width*self.maze_width)
            self.screen_height = int((800+self.maze_height)//self.maze_height*self.maze_height)
            if self.screen_width>max_width:
                self.screen_width = max_width//self.maze_width*self.maze_width
            if self.screen_height>max_height:
                self.screen_height = max_height//self.maze_height*self.maze_height

    def check_maze_size(self):       
        if self.maze_width %2 ==0:
            self.maze_width+=1
        if self.maze_height %2 ==0:
            self.maze_height+=1