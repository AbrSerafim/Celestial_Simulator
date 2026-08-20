""" Handles physics and numerical calculations """

import numpy as np
import scipy 

import bodies

# F = m a = GMm/|r|^3 r

G = 6.6743e-11 #m^3*kg^-1*s^-2

class Simulation():
    """ Object to handle simulation calculations """

    def __init__(self, G=G):
        self.G = G

    def _partial_aceleration(self,
                    mass: float,
                    pos: np.array):
        """ Calculates aceleration from only one body """
        return self.G * mass / (np.linalg.vector_norm(pos)**3) * np.array([
            pos[0], pos[1]
        ], np.float32)

    def aceleration(self,
                    system: bodies.CelestialSystem,
                    body: bodies.CelestialBody):
        """ Superposition of acelerations """
        ac = np.array([0, 0], np.float32)
        for bodies in system.bodies:
            if bodies != body:
                ac += self._partial_aceleration(bodies.mass, bodies.pos)

        return ac

    def velocity(self):
        """ Uses runge-kutta to calculate velocity """
        pass