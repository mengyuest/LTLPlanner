import sys
import numpy as np

from PWLPlan import plan, Node
from vis import vis

def test():
    wall_half_width = 0.05
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    walls = []

    walls.append(np.array([-1.5, -1.5, -1.5, 1.5], dtype = np.float64))
    walls.append(np.array([1.5, 1.5, -1.5, 1.5], dtype = np.float64))
    walls.append(np.array([-1.5, 1.5, -1.5, -1.5], dtype = np.float64))
    walls.append(np.array([-1.5, 1.5, 1.5, 1.5], dtype = np.float64))

    obs = []
    for wall in walls:
        if wall[0]==wall[1]:
            wall[0] -= wall_half_width
            wall[1] += wall_half_width
        elif wall[2]==wall[3]:
            wall[2] -= wall_half_width
            wall[3] += wall_half_width
        else:
            raise ValueError('wrong shape for axis-aligned wall')
        wall *= np.array([-1,1,-1,1])
        obs.append((A, wall))
    # (-x1, x2, -y1, y2)
    b1 = np.array([1.0, -0.5, -0.5, 1], dtype = np.float64)
    B1 = (A, b1)
    b2 = np.array([-0.5, 1, -0.5, 1], dtype = np.float64)
    B2 = (A, b2)
    b3 = np.array([-0.5, 1, 1, -0.5], dtype = np.float64)
    B3 = (A, b3)
    C = np.array([1, -0.5, 1, -0.5], dtype = np.float64)
    C = (A, C)

    x0 = [-0.6, 0.6]

    # goal = [1,1]

    plots = [[[B1,], 'royalblue', 'init', 0.5],
             [[B2,], 'y', 'pear', 0.5],
             [[B3,], 'g', 'house', 0.5],
             [[C,],  'gray', 'obs', 0.5], [obs, 'k']]
    tmax = 10.
    vmax = 10.

    # TODO
    ltl_spec = "F(pear=1 U (F(house=1))"

    # notC = Node('negmu', info={'A':C[0], 'b':C[1]})
    # notB2 = Node('negmu', info={'A': B2[0], 'b': B2[1]})
    # notB3 = Node('negmu', info={'A': B3[0], 'b': B3[1]})
    # B1 = Node('mu', info={'A':B1[0], 'b':B1[1]})
    # B2 = Node('mu', info={'A':B2[0], 'b':B2[1]})
    # B3 = Node('mu', info={'A':B3[0], 'b':B3[1]})

    # phi_1 = Node('F', deps=[Node('U', deps=[B2, B3], info={'int':[0, tmax]}),], info={'int':[0,tmax]})

    # phi_1 = Node('U', deps=[Node('F', deps=[B3,], info={'int': [0, tmax]}),
    #                         Node('F', deps=[B2,], info={'int': [0, tmax]})],
    #              info={'int': [0, tmax]})

    # Fhouse = Node('F', deps=[B2], info={'int':[0, tmax]})
    # pear_U_Fhouse = Node('U', deps=[B3, Fhouse], info={'int': [0, tmax]})
    # phi_1 = Node('F', deps=[pear_U_Fhouse], info={'int': [0, tmax]})

    info = {'int': [0, tmax]}
    spec = def_spec1(B1, B2, B3, C, info)
    # spec = def_spec2(B1, B2, B3, C, info)

    x0s = [x0,]
    specs = [spec,]
    # goals = [goal, ]
    goals = None
    PWL = plan(x0s, specs, bloat=0.05, size=0.11/2, num_segs=4, tmax=tmax, vmax=vmax, hard_goals=goals)

    return x0s, plots, PWL


def def_spec1(B1, B2, B3, C, info):
    # notC = Node('negmu', info={'A': C[0], 'b': C[1]})
    # notB2 = Node('negmu', info={'A': B2[0], 'b': B2[1]})
    # notB3 = Node('negmu', info={'A': B3[0], 'b': B3[1]})
    # B2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    # B3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    # finalB2 = Node('F', deps=[B2], info=info)
    # finalB3 = Node('F', deps=[B3], info=info)
    # phi_reach = Node('U', deps=[B2, finalB3], info=info)
    # phi_1 = Node('U', deps=[notB3, phi_reach], info=info)
    # phi_2 = Node('A', deps=[notC, ], info=info)
    # spec = Node('and', deps=[phi_1, phi_2])

    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    phi_1 = Node('U', deps=[inB2, inB3], info=info)
    spec = Node('F', deps=[phi_1], info=info)
    # spec = Node('F', deps=[inB3], info=info)
    return spec


def def_spec2(B1, B2, B3, C, info):
    notC = Node('negmu', info={'A': C[0], 'b': C[1]})
    notB2 = Node('negmu', info={'A': B2[0], 'b': B2[1]})
    notB3 = Node('negmu', info={'A': B3[0], 'b': B3[1]})
    B2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    B3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    finalB2 = Node('F', deps=[B2], info=info)
    finalB3 = Node('F', deps=[B3], info=info)
    phi_reach = Node('U', deps=[B3, finalB2], info=info)
    phi_1 = Node('U', deps=[notB2, phi_reach], info=info)
    phi_2 = Node('A', deps=[notC, ], info=info)
    spec = Node('and', deps=[phi_1, phi_2])
    return spec


if __name__ == '__main__':
    results = vis(test, ani=True)
