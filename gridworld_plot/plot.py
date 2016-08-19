import pylab as pl 
import numpy as np
import matplotlib.patches as patches
import matplotlib.cm as cm

from matplotlib.text import OffsetFrom
from matplotlib.patches import Arrow

def plot_num(ax, xy, offset, value):
    x, y = xy
    offset = offset * .47

    textoffset = offset *.85
    textxy = (x + textoffset[0], y + textoffset[1])

    ax.annotate(value, 
            xy=(x, y), xycoords='data',
            xytext=textxy,
            horizontalalignment='center',
            verticalalignment='center')

def plot_arrow(ax, xy, offset, color):
    x, y = xy
    offset = offset * .47

    arrowx = x + offset[0]*.15
    arrowy = y + offset[1]*.15
    ax.add_patch(
            Arrow(arrowx, arrowy, offset[0]*.8, offset[1]*.8, width=.5, facecolor=color))

def color_square(ax, xy, color):
    x, y = xy
    ax.add_patch(
        patches.Rectangle(
            (x, y),   # (x,y)
            .99,          # width
            .99,          # height
            color=color
        )
    )

def plot_labeled_arrows(ax, xy, qs): 
    dirs = [LEFT, DOWN, RIGHT, UP]

    for q, direction in zip(qs, dirs):
        plot_arrow(ax, xy, direction, cm.plasma(q * .75 + .25))
        plot_num  (ax, xy, direction, "%.3g" % q)



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
    vals = compute_vals(Qs)
    vmax, vmin = max(vals), min(vals)
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

def plotR(ax, gridworld, R, Rs):
    for s in range(gridworld.nState): 
        r = R[s, 0]
        rs = (Rs[s,0][0],)

        rc = gridworld.row_and_column(s)
        xy = rowcol_to_xy(gridworld, rc + np.array([.25, .25]) )

        plot_num(ax, xy, "%.3g ~ %.3g, %.3g" % (rs +r))

def grid_plot(gridworld):
    fig = pl.figure() 
    ax = fig.add_subplot(111)

    ax.set_xticks(range(gridworld.grid_width +1))
    ax.set_yticks(range(gridworld.grid_width + 1))
    pl.grid(True)
    return fig, ax
    
