""" Debugging and visualization tools for the simulation """

import numpy as np
import matplotlib.pyplot as plt

def plot_rk_debug(debug_states: np.array,
                  num_bodies: int) -> None:
    """ Plot the internal states evaluated by RK45 """
    """ NOTE: Not handling when a body is removed mid simulation """

    times = np.array([ # Extracts time 't' used by _derivative
        entry["time"]
        for entry in debug_states
    ])

    states = np.array([ # Exctracts state itself
        entry["state"]
        for entry in debug_states
    ])

    if len(times) != len(states):
        raise ValueError(
            "'times' and 'states' mus have the same number of entries"
            )

    if states.shape[1] != num_bodies * 4:
        raise ValueError(
            f"Expected state size {num_bodies*4}, "
            f"got {states.shape[1]}"
        )

    # ---------------------------------------------------------
    # Position (y & x vs t)
    # ---------------------------------------------------------

    plt.figure()

    for i in range(num_bodies):
        idx = i*4

        x = states[:, idx]
        y = states[:, idx + 1]

        plt.plot(times, x, label=f"Body {i} x")
        plt.plot(times, y, label=f"Body {i} y")

    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.title("Position Evaluations")
    plt.legend()
    plt.grid()

    # ---------------------------------------------------------
    # Velocity (vy & vx vs t)
    # ---------------------------------------------------------

    plt.figure()

    for i in range(num_bodies):
        idx = i*4

        vx = states[:, idx + 2]
        vy = states[:, idx + 3]

        plt.plot(times, vx, label=f"Body {i} Vx")
        plt.plot(times, vy, label=f"Body {i} Vy")

    plt.xlabel("Time")
    plt.ylabel("Velocity")
    plt.title("Velocity Evaluations")
    plt.legend()
    plt.grid()

    # ---------------------------------------------------------
    # Trajectory (y vs x)
    # ---------------------------------------------------------

    plt.figure()

    for i in range(num_bodies):
        idx = i*4

        x = states[:, idx ]
        y = states[:, idx + 1]

        plt.plot(x, y, label=f"Body {i}")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Trajectory Evaluations")
    plt.legend()
    plt.grid()

    plt.show()

if __name__ == "__main__":
    pass