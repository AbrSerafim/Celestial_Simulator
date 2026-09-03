""" Define and qualify celestial entities objects """

import numpy as np

class CelestialBody():
    """ Basic unit of the simulation """

    def __init__(
            self,
            name: str, 
            mass: float,
            radius: float,
            pos: np.array, # (x,y)
            vel: np.array = np.array([0, 0], dtype=np.float32), # (vx, vy)
            ac: np.array = np.array([0, 0],dtype=np.float32) # (ax,ay)
            ):
        self.name = name
        self.mass = mass
        self.radius = radius 
        self.pos = pos
        self.vel = vel
        self.ac = ac

    def update_ac(self, new_ac: np.array): # Not used so far
        """ Updates the body acceleration """
        self.ac = new_ac

    def update_vel(self, new_vel: np.array):
        """ Updates the body velocity """
        self.vel = new_vel

    def update_pos(self, new_pos: np.array):
        """ Updates the body position """
        self.pos = new_pos

class CelestialSystem():
    """ Composition of CelestialBody's """

    def __init__(
            self,
            name: str,
            bodies: list = [],
            time: np.float64 = 0,
            time_history: np.array = None,
            history: np.array = None):
        self.name = name
        self.bodies = bodies
        self.time = np.float64(time)
        if (history == None) and (time_history == None):
            self.history = np.empty((0, 0), dtype=np.float64)
            self.time_history = np.empty(0, dtype=np.float64)
        else: 
            self.history = history
            self.time_history = time_history

    def clear_system(self): 
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
        self.history = np.hstack([ # Corrects history shape so it doesn't the pipeline
            self.history,
            np.full((self.history.shape[0],4), np.nan, dtype=np.float64)
        ])

    """ Check how to handle 'history' after removing body """

    def remove_body(self, body_name: str):  
        """ Remove a body from the system """
        """ NOTE: It also deletes its history """
        for x in self.bodies:
            if x.name == body_name:
                index = self.bodies.index(x)
                self.bodies.pop(index)

                self.history = np.delete(
                    self.history,
                    np.s_[index*4:(index*4) + 4],
                    axis=1
                )

    def clear_history(self):
        """ Erases all previous system simulation data """

        self.history = np.empty(
            (0, len(self.bodies) * 4),
            dtype=np.float64
        )

        self.time = 0
        self.time_history = np.empty(0, dtype=np.float64)

    def _record_state(self, state: np.array):
        """ Saves simulation 'state' onto system history """
        
        self.history = np.vstack([
            self.history,
            state
        ])

        self.time_history = np.append(self.time_history, self.time)


if __name__ == "__main__":
    pass