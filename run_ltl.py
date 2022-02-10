import sys
import numpy as np

from PWLPlan import plan, Node
from vis import vis
import pypoman as ppm
import matplotlib.pyplot as plt
import os

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
    # b1 = np.array([1.0, -0, -0, 1], dtype=np.float64)
    b1 = np.array([1.0, -0.5, -0.5, 1], dtype=np.float64)
    B1 = (A, b1)
    # b2 = np.array([-0, 1, -0, 1], dtype=np.float64)
    b2 = np.array([-0.5, 1, -0.5, 1], dtype=np.float64)
    B2 = (A, b2)
    # b3 = np.array([-0, 1, 1, 0], dtype = np.float64)
    b3 = np.array([-0.5, 1, 1, -0.5], dtype=np.float64)
    B3 = (A, b3)
    # C = np.array([1, -0, 1, -0], dtype = np.float64)
    C = np.array([1, -0.5, 1, -0.5], dtype=np.float64)
    C = (A, C)


    x0 = [-0.6, 0.6]
    x1 = [0.75, 0.75]

    plots = [[[B1,], 'royalblue', 'init', 0.5],
             [[B2,], 'y', 'pear', 0.5],
             [[B3,], 'g', 'house', 0.5],
             [[C,],  'orange', 'orange', 0.5], [obs, 'k']]
    tmax = 4.
    vmax = 4.

    x0s = [x0, ]
    x1s = [x1,]
    goals = None
    info = {'int': [0, tmax]}

    # spec = def_spec1(B1, B2, B3, C, info)
    # plan_vis("cache_1", "In due time, reach the house and eventually collect the pear \nF (house U pear)", spec, x0s, plots, tmax, vmax)

    # spec = def_spec2(B1, B2, B3, C, info)
    # plan_vis("cache_2", "At some point, start going to the house \nF (house)", spec, x0s, plots, tmax, vmax)

    # spec = def_spec3(B1, B2, B3, C, info)
    # plan_vis("cache_3", "Grasp the pear and persist\nG (pear)", spec, x1s, plots, tmax, vmax)

    # spec = def_spec4(B1, B2, B3, C, info)
    # plan_vis("cache_4", "Repeatedly go to the house \nG F (house)", spec, x0s, plots, tmax, vmax, num_segs=4)

    # spec = def_spec5(B1, B2, B3, C, info)
    # plan_vis("cache_5", "Take the pear or the orange \nF (pear | orange)", spec, x0s, plots, tmax, vmax, num_segs=4)

    spec = def_spec6(B1, B2, B3, C, info)
    plan_vis("cache_6", "Always go to the pear and the house\nG (F (house) & F (pear))", spec, x0s, plots, tmax, vmax)



def plan_vis(dirname ,ltl_str, spec, x0s, plots, tmax, vmax, num_segs=4):
    print(dirname, ltl_str)
    specs = [spec, ]
    PWL = plan(x0s, specs, bloat=0, size=0, num_segs=num_segs, tmax=tmax, vmax=vmax, hard_goals=None)
    if PWL[0] is None:
        PWL = [[x0s]]
    vis_here(PWL, plots, ltl_str, dirname, limits=None, equal_aspect=True, ani=True)


## F (pear U house)
# def def_spec1(B1, B2, B3, C, info):
#     inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
#     inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
#     phi_1 = Node('U', deps=[inB2, inB3], info=info)
#     spec = Node('F', deps=[phi_1], info=info)
#     return spec

## F (pear U (F house))
# def def_spec1(B1, B2, B3, C, info):
#     inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
#     inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
#     FinB3 = Node('F', deps=[inB3], info=info)
#     phi_1 = Node('U', deps=[inB2, FinB3], info=info)
#     spec = Node('F', deps=[phi_1], info=info)
#     return spec

##  F(house U pear) // until as F (0, t0) & F (t1, tmax)
def def_spec1(B1, B2, B3, C, info):
    tmax=info['int'][1]
    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    FinB2 = Node('F', deps=[inB3], info={'int': [0, tmax//2]})
    FinB3 = Node('F', deps=[inB2], info={'int': [tmax//2, tmax]})
    # phi_1 = Node('U', deps=[inB2, FinB3], info=info)
    spec = Node('and', deps=[FinB2, FinB3])
    return spec

# F(house)
def def_spec2(B1, B2, B3, C, info):
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    spec = Node('F', deps=[inB3], info=info)
    return spec

# G (pear)
def def_spec3(B1, B2, B3, C, info):
    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    spec = Node('A', deps=[inB2], info=info)
    return spec

# G F (house)
def def_spec4(B1, B2, B3, C, info):
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    FinB3 = Node('F', deps=[inB3], info=info)
    spec = Node('A', deps=[FinB3], info=info)
    return spec

# F (pear | orange)
def def_spec5(B1, B2, B3, C, info):
    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    inC = Node('mu', info={'A': C[0], 'b': C[1]})
    inB2_or_C = Node('or', deps=[inB2, inC])
    spec = Node('F', deps=[inB2_or_C], info=info)
    return spec


# G (F (house) & F (pear))
def def_spec6(B1, B2, B3, C, info):
    inB2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
    inB3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
    FinB2 = Node('F', deps=[inB2], info=info)
    FinB3 = Node('F', deps=[inB3], info=info)
    FinB2_and_B3 = Node('and', deps=[FinB2, FinB3])
    spec = Node('A', deps=[FinB2_and_B3], info=info)
    return spec


# def def_spec2(B1, B2, B3, C, info):
#     notC = Node('negmu', info={'A': C[0], 'b': C[1]})
#     notB2 = Node('negmu', info={'A': B2[0], 'b': B2[1]})
#     notB3 = Node('negmu', info={'A': B3[0], 'b': B3[1]})
#     B2 = Node('mu', info={'A': B2[0], 'b': B2[1]})
#     B3 = Node('mu', info={'A': B3[0], 'b': B3[1]})
#     finalB2 = Node('F', deps=[B2], info=info)
#     finalB3 = Node('F', deps=[B3], info=info)
#     phi_reach = Node('U', deps=[B3, finalB2], info=info)
#     phi_1 = Node('U', deps=[notB2, phi_reach], info=info)
#     phi_2 = Node('A', deps=[notC, ], info=info)
#     spec = Node('and', deps=[phi_1, phi_2])
#     return spec



def vis_here(PWLs, plots, ltl_str, dirname, limits=None, equal_aspect=True, ani=False):
    os.makedirs(dirname, exist_ok=True)
    print(PWLs)
    plt.rcParams["figure.figsize"] = [6.4, 6.4]
    plt.rcParams['axes.titlesize'] = 20

    # TODO(yue)
    ts = range(len(PWLs[0]))

    for ti in range(len(ts)):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.axis('off')

        vertices = []
        for plot in plots:
            for A, b in plot[0]:
                vs = ppm.duality.compute_polytope_vertices(A, b)
                vertices.append(vs)
                if len(plot) > 3: # TODO (yue)
                    ppm.polygon.plot_polygon(vs, color=plot[1], alpha=plot[3])
                else:
                    ppm.polygon.plot_polygon(vs, color = plot[1], alpha=1.)
                # TODO (yue)
                if len(plot)>2:
                    x_text = (b[1]-b[0])/2
                    y_text = (b[3]-b[2])/2
                    text = plot[2]
                    plt.text(x_text, y_text, text, fontsize=16, ha="center")

        if limits is not None:
            plt.xlim(limits[0])
            plt.ylim(limits[1])
        else:
            vertices = np.concatenate(vertices, axis=0)
            xmin, ymin = vertices.min(axis=0)
            xmax, ymax = vertices.max(axis=0)
            plt.xlim([xmin - 0.1, xmax + 0.1])
            plt.ylim([ymin - 0.1, ymax + 0.1])

        if equal_aspect:
            plt.gca().set_aspect('equal', adjustable='box')

        if PWLs is None or PWLs[0] is None:
            plt.show()
            return

        if len(PWLs) <= 4:
            colors = ['k', np.array([153,0,71])/255, np.array([6,0,153])/255, np.array([0, 150, 0])/255]
        else:
            cmap = plt.get_cmap('tab10')
            colors = [cmap(i) for i in np.linspace(0, 0.85, len(PWLs))]

        for i in range(len(PWLs)):
            PWL = PWLs[i]
            ax.plot([P[0][0] for P in PWL], [P[0][1] for P in PWL], '-', color = colors[i])
            ax.plot(PWL[-1][0][0], PWL[-1][0][1], '*', color=colors[i])
            ax.plot(PWL[0][0][0], PWL[0][0][1], 'o', color=colors[i])
        PWL = PWLs[0]
        ax.plot(PWL[ti][0][0], PWL[ti][0][1], '>', color="red", markersize=12)
        plt.title("%s\nTrace (t=%d/%d)" % (ltl_str, ti, len(ts)), fontsize=18)
        plt.savefig("%s/fig_%04d.png" % (dirname, ti), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    os.system("convert -delay 50 -loop 0 %s/*.png %s/animation.gif"%(dirname, dirname))

if __name__ == '__main__':
    # results = vis(test, ani=True)
    test()