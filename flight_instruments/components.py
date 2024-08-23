from __future__ import annotations
from pygame import Surface
from typing import NewType

Coordinate = NewType('Coordinate', tuple)
#TODO: Get rid of this class. When can use surface.get_rect().center/topleft, etc to get the coordinates we want
#custom surface with some useful methods 
class CSurface(Surface):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
    
    
    def get_coord_at_fraction(self, f_width: float, f_height: float) -> Coordinate:

        return (int(f_width * self.get_width()), f_height * self.get_height())
    
    @property
    def center(self) -> Coordinate:

        # return self.get_coord_at_fraction(0.5, 0.5)
        return self.get_rect().center
    
    @property
    def center_left(self) -> Coordinate:

        return self.get_coord_at_fraction(0.0, 0.5)
    
    @property
    def center_right(self) -> Coordinate:
        
        return self.get_coord_at_fraction(1, 0.5)
    
    def blit_centered(self, surface: CSurface ,*args, **kwargs) -> None:
        
        dest_x = self.center[0] - surface.center[0]
        dest_y = self.center[1] - surface.center[1]
        
        self.blit(surface, dest = (dest_x, dest_y), *args, **kwargs)

    
    