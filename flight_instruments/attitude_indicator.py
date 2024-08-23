import pygame
from pygame import Surface
from pygame import gfxdraw
from math import pi

from flight_instruments.components import CSurface


def draw_gradient(surface: CSurface, start_color: tuple, end_color: tuple):
    """ Draw a vertical gradient from start_color to end_color """
    for y in range(surface.get_height()):
        # Calculate the ratio of the current line to the total height
        
        ratio = y / surface.get_height()
        
        # Calculate the new color based on the ratio
        new_color = (
            int(start_color[0] * (1 - ratio) + end_color[0] * ratio),
            int(start_color[1] * (1 - ratio) + end_color[1] * ratio),
            int(start_color[2] * (1 - ratio) + end_color[2] * ratio),
        )
        # Draw the line with the new color
        pygame.draw.line(surface, new_color, (0, y), (surface.get_width(), y))
    
    return surface

def make_aircraft_marker(width: int, height: int) -> CSurface:
        
        surface = CSurface((width, height), pygame.SRCALPHA)
        ## Centered square
        square_size = 10
        x_center, y_center = surface.center[0] - square_size/2, surface.center[1] - square_size/2
        pygame.draw.rect(surface, color = (255,255,255),
            rect = (x_center, y_center, square_size, square_size))
        
        _wing_surf = CSurface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        
        _wing_surf.fill((0,0,0,0))

        # 'right wing'
        pygame.draw.rect(_wing_surf, color = (255,255,255), rect = (x_center + 4*square_size, y_center, 10*square_size, square_size))
        pygame.draw.rect(_wing_surf, color = (255,255,255), rect = (x_center + 4*square_size, y_center, square_size, 2*square_size))
        
        #blitting symetric regarding x
        _wing_surf.blit(
            pygame.transform.flip(_wing_surf.copy(), True, False),
            (0,0))
        
        surface.blit(_wing_surf, (0,0))
        
        return surface

def make_horizon_surface(
    width: int, height: int, 
    light_blue: tuple, blue: tuple,
    light_brown: tuple, brown: tuple) -> CSurface:
    
    background = CSurface((width, height), pygame.SRCALPHA)
        
    _brown_surf = CSurface((width, height/2))
    _brown_surf.fill(brown)
    _grad_brown = draw_gradient(CSurface((width, height/4)), brown, light_brown)
    _brown_surf.blit(_grad_brown, ((0,_brown_surf.get_height()/2)))

    _blue_surf = CSurface((width, height/2))
    _blue_surf.fill(blue)
    _grad_blue = draw_gradient(CSurface((width, int(height/4))), blue, light_blue)
    _blue_surf.blit(_grad_blue, (0,_blue_surf.get_height()/2))
    
    background.blit(_blue_surf, (0,0))
    background.blit(pygame.transform.flip(_brown_surf, False, True), (0, height/2))
    
    pygame.draw.line(background, (255,255,255), background.get_rect().midleft, background.get_rect().midright, 2)

    return background


def make_pitch_indicator(width: int, height: int) -> CSurface:
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 20)
    
    _text_10 = font.render('10', True, (255, 255, 255, 175))

    surf = CSurface((width, height), pygame.SRCALPHA)
    _x_shift = 20
    half_line_len = int(width/6) 
    angs = [5, 10, 15]
    for i, ang_deg in enumerate(angs):
        
        if i%2 == 1: 
            half_line_len = int(width/6) - 10 
        else: 
            half_line_len = int(width/12) - 5
        
        alpha = (1-i/len(angs)) * 100 + 75
        
        y = surf.get_rect().midleft[1] - 30*(i+1)

        pygame.draw.line(surf, (255,255,255, alpha),
            start_pos = (surf.get_rect().center[0] - half_line_len, y),
            end_pos=(surf.get_rect().center[0] + half_line_len , y),
            width = 3)
    
    surf.blit(pygame.transform.flip(surf, False, True), (0,0))
    
    # Drawing the text
    surf.blit(_text_10, (surf.get_rect().center[0] - half_line_len - 95, surf.get_rect().midleft[1] - 80))
    surf.blit(_text_10, (surf.get_rect().center[0] + half_line_len  + 75, surf.get_rect().midleft[1] - 80))
    surf.blit(_text_10, (surf.get_rect().center[0] - half_line_len - 95, surf.get_rect().midleft[1] + 40))
    surf.blit(_text_10, (surf.get_rect().center[0] + half_line_len + 75, surf.get_rect().midleft[1] + 40))
    

    return surf
    

def make_roll_scale(width: int, height: int) -> CSurface:
    
    deg2rad = pi / 180
    surf = CSurface((width, height), pygame.SRCALPHA)
    
    radius = 300
    origin = (int(0.5*width) - radius, int(0.2*surf.get_rect().center[1]))
    pygame.draw.arc(surf, (255,255,255, 150), (*origin, 2*radius, 2*radius), (-65 + 90) * deg2rad, (65 + 90) * deg2rad, 2)
    # pygame.draw.arc(surf, (255,255,255), (*origin, 2*radius, 2*radius), (0) * deg2rad, (360) * deg2rad, 2)
    
    ## Drawing the roll scale
    ang_step = 20
    p0 = pygame.Vector2(*surf.get_rect().center)
    p_end = pygame.Vector2(*surf.get_rect().midtop)
    v = pygame.Vector2((0, -radius)).rotate(-60)
    
    for ang in range(7):
        
        v_start = v + p0
        v_end = v_start + v_start.normalize() *  10

        pygame.draw.line(surf, (255,255,255, 150), (v_start.x, v_start.y), (v_end.x, v_end.y), 2)
        # pygame.draw.line(surf, (255,255,255, 150), (p0.x, p0.y), (p0.x + v.x, p0.y  + v.y), 2)
        v = v.rotate(ang_step)
        
    

    return surf

# def _draw_numeric_indicator(self, surface: CSurface, indicator_width: int, indicator_height: int, dest: tuple) -> None:
    
#     indicator_surf = CSurface((indicator_width, indicator_height), pygame.SRCALPHA)
    
#     indicator_surf.fill((0,0,0, 150))
#     surface.blit(
#         indicator_surf,
#         dest)


class AttitudeIndicator:
    
    blue = (18, 108, 178)
    light_blue = (120, 170, 200)

    brown = (180,90,45)
    light_brown = (200,150,15)
    

    def __init__(self, width: int = 600, height: int = 600) -> None:

        self.width = width
        self.height = height
        self._horizon = make_horizon_surface(
            2 * self.width, 2 * self.height,
            self.light_blue, self.blue, self.light_brown, self.brown)
        
        self._aircraft_marker_surface = make_aircraft_marker(self.width, self.height)
        self._pitch_indicator = make_pitch_indicator(self.width, self.height)
        self._roll_scale = make_roll_scale(self.width, self.height)
        

        # self._draw_numeric_indicator(self.horizon, 60, 250, dest = (2, int((self.horizon.get_height() - 250)/2)))
        # self._draw_numeric_indicator(self.horizon, 60, 250, dest = (self.horizon.get_width() - 62, int((self.horizon.get_height() - 250)/2)))
    
    @property
    def horizon_origin(self) -> tuple:
        return (-self.width/2, -self.height/2)
    
    @property
    def horizon(self) -> CSurface:
        return self._horizon.copy()
    
    def get_pitch_indicator(self) -> CSurface:        
        return self._pitch_indicator.copy()
    
    def get_roll_scale(self) -> CSurface:
        return self._roll_scale.copy()
    
    def get_horizon(self, row_deg: float = 0.0, pitch_deg: float = 0.0) -> CSurface:
        
        hrz = CSurface((self.width, self.height))
        ##* rotate is performs a counterclockwise rotation
        
        _hr_rotated = self.horizon
        _hr_rotated.blit(self.get_pitch_indicator(), (self.horizon.get_width()/4, self.horizon.get_height()/4))
        _hr_rotated = pygame.transform.rotate(_hr_rotated, row_deg)
        
        y_shift = int(self.height/2) * (pitch_deg/45)
        new_topleft = (self.horizon_origin[0], self.horizon_origin[1] + y_shift)
        _hr_new_rect = _hr_rotated.get_rect(center = self.horizon.get_rect(topleft = new_topleft).center)
        
        hrz.blit(_hr_rotated, _hr_new_rect.topleft)
        
        return hrz
    
    def get_screen(self, row_deg: float = 0.0, pitch_deg: float = 0.0) -> CSurface:
        
        scr = CSurface((self.width, self.height)) 
        hrz = self.get_horizon(row_deg, pitch_deg)

        scr.blit(hrz, (0,0))
        # scr.blit(self.get_roll_scale(), (0 , 0))
        scr.blit(self._aircraft_marker_surface, (0,0))
        
        return scr
        
    
