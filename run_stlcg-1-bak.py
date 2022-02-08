import sys
import numpy as np

from PWLPlan import plan, Node
from vis import vis

def test():
    wall_half_width = 0.05
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    walls = []

    walls.append(np.array([-1.5, -1.5, -1.5, 1.5], dtype=np.float64))
    walls.append(np.array([1.5, 1.5, -1.5, 1.5], dtype=np.float64))
    walls.append(np.array([-1.5, 1.5, -1.5, -1.5], dtype=np.float64))
    walls.append(np.array([-1.5, 1.5, 1.5, 1.5], dtype=np.float64))

    obs = []
    for wall in walls:
        if wall[0] == wall[1]:
            wall[0] -= wall_half_width
            wall[1] += wall_half_width
        elif wall[2] == wall[3]:
            wall[2] -= wall_half_width
            wall[3] += wall_half_width
        else:
            raise ValueError('wrong shape for axis-aligned wall')
        wall *= np.array([-1, 1, -1, 1])
        obs.append((A, wall))
    # (-x1, x2, -y1, y2)
    b1 = np.array([1.0, -0.5, -0.5, 1], dtype=np.float64)
    B1 = (A, b1)
    b2 = np.array([-0.5, 1, -0.5, 1], dtype=np.float64)
    B2 = (A, b2)
    b3 = np.array([-0.5, 1, 1, -0.5], dtype=np.float64)
    B3 = (A, b3)
    C = np.array([1, -0.5, 1, -0.5], dtype=np.float64)
    C = (A, C)

    x0 = [-0.6, 0.6]

    plots = [[[B1, ], 'royalblue', 'init', 0.5],
             [[B2, ], 'y', 'pear', 0.5],
             [[B3, ], 'g', 'house', 0.5],
             [[C, ], 'gray', 'obs', 0.5], [obs, 'k']]
    tmax = 10.
    vmax = 10.

    # First reach pear then reach house
    # F (Pear U House)
    info = {'int': [0, tmax]}
    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    phi_1 = Node('U', deps=[inB2, inB3], info=info)
    spec = Node('F', deps=[phi_1,], info=info)

    x0s = [x0, ]
    specs = [spec, ]
    goals = None
    PWL = plan(x0s, specs, bloat=0.05, size=0.11 / 2, num_segs=5, tmax=tmax, vmax=vmax, hard_goals=goals)

    return x0s, plots, PWL


if __name__ == '__main__':
    results = vis(test)
