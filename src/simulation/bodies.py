""" Define and qualify celestial entities objects """

import numpy as np

class CelestialBody():
    """ Basic unit of the simulation """

    def __init__(
            self,
            name: str, 
            mass: float,
            radius: float,
            pos: np.array,
            vel: np.array):
        self.name = name
        self.mass = mass
        self.radius = radius 
        self.pos = pos
        self.vel = vel

    def update_vel(self, new_vel: np.array):
        """ Updates the body velocity
            the new vel is obtained by the rk4 solution"""
        self.vel = new_vel

class CelestialSystem():
    """ Composition of CelestialBody's """

    def __init__(
            self,
            name: str,
            bodies: list,
            time: float):
        self.name = name
        self.bodies = bodies
        self.time = time

    def clean_system(self): 
        """ Erases all bodies from a system """
        self.bodies.clear()

    def add_body(self,
            name: str, 
            mass: float,
            radius: float,
            pos: np.array,
            vel: np.array):
        """ Adds a body to the system """
        self.bodies.append(CelestialBody(name, mass, radius, pos, vel))

    def remove_body(self, body_name: str):  
        """ Remove a body from the system """
        for x in self.bodies:
            if x.name == body_name:
                self.bodies.remove(x)
