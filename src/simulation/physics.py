""" Handles physics and numerical calculations """

import numpy as np
from scipy.integrate import solve_ivp

import bodies

# F = m a = GMm/|r|^3 r

class Simulation():
    """ Object to handle simulation calculations """

    def __init__(self,
                 G=6.6743e-11, #m^3*kg^-1*s^-2
                 STEP=15e-3 #s
                ):
        self.G = np.float64(G)
        self.STEP = np.float64(STEP)

    def _get_state(self, system: bodies.CelestialSystem) -> np.array:
        """ Convert the system's bodies into a single state vector """

        state = []

        for body in system.bodies:
            state.extend([
                body.pos[0],
                body.pos[1],
                body.vel[0],
                body.vel[1],
            ])

        return np.array(state, dtype=np.float64)

    def _update_system(self,
                       system: bodies.CelestialSystem,
                       state: np.array):
        """ Update all bodies from an integrated state vector"""

        for i, body in enumerate(system.bodies):

            idx = i*4

            body.update_pos(state[idx: idx + 2])
            body.update_vel(state[idx + 2: idx + 4])

    def _acceleration(self,
                    state: np.array,
                    system: bodies.CelestialSystem) -> np.array:
        """ Calculates acceleration of all bodies """

        n = len(system.bodies)

        positions = np.zeros((n, 2), dtype=np.float64)

        for i in range(n):
            idx = i*4
            positions[i] = state[idx:idx + 2]

        accelerations = np.zeros_like(positions)

        for i, body in enumerate(system.bodies):
            for j, other in enumerate(system.bodies):
                if i == j:
                    continue

                r = positions[j] - positions[i] # From i -> j

                accelerations[i] += (
                    self.G
                    * other.mass
                    * r
                    / np.linalg.norm(r)**3
                )

        return accelerations

    def _derivative(self,
                    t,
                    state: np.array,
                    system: bodies.CelestialSystem):
        """ Defines the callable for the IVP solver """

        acceleration = self._acceleration(state=state, system=system)

        derivative = np.zeros_like(state)

        for i in range(len(system.bodies)):

            idx = i * 4

            # dr/dt = v
            derivative[idx], derivative[idx + 1] = state[idx + 2], state[idx + 3]

            # dv/dt = a
            derivative[idx + 2], derivative[idx + 3] = acceleration[i, 0], acceleration[i, 1]

        return derivative

    def step(self, system: bodies.CelestialSystem) -> np.array:
        """ Updates state by a singular step """

        state_0 = self._get_state(system=system)

        solution = solve_ivp(
            lambda t, state: self._derivative(t, state=state, system=system),
            t_span=(system.time, system.time + self.STEP),
            y0=state_0,
            method="RK45",
            rtol=1e-9,
            atol=1e-9
        )

        final_state = solution.y[:, -1]

        self._update_system(system=system, state=final_state)

        system.time += self.STEP

        return solution

""" For simulation loop

    sim = Simulation()

    while running:
        
        simulation.step(system)

    Render system 
"""