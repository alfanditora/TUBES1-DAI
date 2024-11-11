import random
import json

class MagicCube(object):
    def __init__(self, cube=None):
        if cube is None:
            self.size = 5
            self.cube = self.create_random_cube()
        else:
            self.size = 5
            self.cube = cube
        self.magic_number = 315
        self.value = self.calculate_value()
    
    # ... [semua method yang sudah ada tetap sama] ...

    def to_dict(self):
        """Convert cube state to dictionary for serialization"""
        return {
            'cube': self.cube,
            'value': self.value,
            'size': self.size,
            'magic_number': self.magic_number
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create cube from dictionary"""
        cube = cls(data['cube'])
        return cube