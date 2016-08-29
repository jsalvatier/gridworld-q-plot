import pylab as pl 
import numpy as np
import matplotlib.patches as patches
import matplotlib.cm as cm

from matplotlib.text import OffsetFrom
from matplotlib.patches import Arrow

def plot_num(ax, xy, offset, value, **kwargs):
    x, y = xy
    offset = offset * .47

    textxy = (x + offset[0]*.85, y + offset[1]*.85)

    ax.annotate(value, 
            xy=(x, y), xycoords='data',
            xytext=textxy,
            horizontalalignment='center',
            verticalalignment='center', **kwargs)

def plot_arrow(ax, xy, offset, color):
    x, y = xy
    offset = offset * .47

    arrowx = x + offset[0]*.65
    arrowy = y + offset[1]*.65
    ax.add_patch(
            Arrow(arrowx, arrowy, offset[0]*.35, offset[1]*.35, width=.5, facecolor=color))

def plot_square(ax, xy, offset, color):
    x, y = xy
    offset = offset * .47

    x = x + offset[0]*.15
    y = y + offset[1]*.15

    ax.add_patch(
        patches.Rectangle(
            (x-.05, y-.05),   
            .1,          # width
            .1,          # height
            facecolor=color,
            edgecolor='black'
        )
    )

def color_square(ax, xy, color):
    x, y = xy
    ax.add_patch(
        patches.Rectangle(
            (x-.5, y-.5),   
            .99,          # width
            .99,          # height
            color=color,
            alpha=.5
        )
    )


def plot_labeled_arrows(dirs): 
    def draw(ax, xy, qs):

        color_square(ax, xy, cm.coolwarm(max(qs)))

        for q, direction in zip(qs, dirs):
            v = (q-min(qs))/(max(qs)-min(qs))
            if not all(direction == CENTER):
                plot_arrow(ax, xy, direction, cm.coolwarm(v))
            else:
                plot_square(ax, xy, direction, cm.coolwarm(v))

            plot_num  (ax, xy, direction, "%.3g" % q)
    return draw



def rowcol_to_xy(gridworld, rowcol):
    row, col = rowcol
    return col + .5, gridworld.grid_width - row - 1 + .5, 


CENTER  = np.array((0. ,  0))
LEFT    = np.array((-1.,  0))
RIGHT   = np.array((1. ,  0))
UP      = np.array((0. ,  1))
DOWN    = np.array((0. , -1))

def compute_vals(qs): 
    return [max(qlist) for qlist in qs.values()]


def normalize_q(Qs): 
    #vals = compute_vals(Qs)
    allq = [q for qs in Qs.values() for q in qs]
    #vmax, vmin = max(vals), min(vals)
    vmax, vmin = max(allq), min(allq)
    range = max(vmax - vmin, 1e-8)

    def norm(q):
        return (q - vmin)/range

    return {s : map(norm, qs) for s, qs in Qs.iteritems() }


def plotQ(ax, gridworld, qs, plot_square): 
    qs = normalize_q(qs)

    for s in range(gridworld.nState): 
        rc = gridworld.row_and_column(s)
        xy = rowcol_to_xy(gridworld, rc)

        plot_square(ax, xy, qs[s])

def plotR(ax, gridworld, Rs):
    for s in range(gridworld.nState): 
        rs = Rs[s,0][0]

        rc = gridworld.row_and_column(s)
        xy = rowcol_to_xy(gridworld, rc)

        plot_num(ax, xy, (UP + RIGHT)*.5, "r=%.3g" % rs, alpha=.5)

def plotRBelief(ax, gridworld, Rs):
    for s in range(gridworld.nState): 
        m, precision = Rs[s,0]
        sd = precision **-.5


        rc = gridworld.row_and_column(s)
        xy = rowcol_to_xy(gridworld, rc)



        plot_num(ax, xy, (.5*UP + RIGHT)*.5, "[%.3g, %.3g]" % (m-sd, m+sd))

def grid_plot(gridworld):
    fig = pl.figure() 
    ax = fig.add_subplot(111)

    coords = [ gridworld.row_and_column(s) for s in range(gridworld.nState) ]
    rmax = max(c[0] for c in coords)
    cmax = max(c[1] for c in coords)
    ax.set_xticks(range(cmax + 2))
    ax.set_yticks(range(rmax + 2))
    pl.grid(True)
    return fig, ax
    
