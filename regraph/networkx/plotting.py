"""Collection of utils for plotting various regraph objects."""
import copy

import networkx as nx
import numpy as np

from regraph.utils import keys_by_value
from matplotlib import pyplot as plt


def _ticks_off():
    plt.tick_params(
        axis='x',           # changes apply to the x-axis
        which='both',       # both major and minor ticks are affected
        bottom='off',       # ticks along the bottom edge are off
        top='off',          # ticks along the top edge are off
        labelbottom='off')  # labels along the bottom edge are off
    plt.tick_params(
        axis='y',           # changes apply to the x-axis
        which='both',       # both major and minor ticks are affected
        left='off',         # ticks along the bottom edge are off
        right='off',        # ticks along the top edge are off
        labelleft='off')    # labels along the bottom edge are off


def _set_limits(nodes, labels, margin=0.1):
    xmin = min([
        p[0] for _, p in nodes.items()
    ])
    xmax = max([
        p[0] for _, p in nodes.items()
    ])
    ymin = min([
        p[1] for _, p in nodes.items()
    ])
    ymax = max([
        p[1] for _, p in labels.items()
    ])

    plt.xlim([
        xmin - margin * abs(xmax - xmin),
        xmax + margin * abs(xmax - xmin)
    ])
    plt.ylim([
        ymin - margin * abs(ymax - ymin),
        ymax + margin * abs(ymax - ymin)
    ])
    return


def plot_graph(graph, filename=None, parent_pos=None, title=None):
    """Plot networkx graph.

    If `filename` is specified, saves the plot into the file,
    otherwise invokes `matplotlib.pylab.show` function
    (shows the plot). In addition, this function allows to
    specify user defined position for some subset of
    graphs nodes (with `parent_pos` parameter), nodes
    whose positioning is not specified in `parent_pos` are
    placed using `nx.spring_layout` function.

    Parameters
    ----------
    graph : nx.(Di)Graph
        Graph object to plot
    filename : str, optional
        Path to file to save the plot
    parent_pos : dict, optional
        Dictionary containing positioning of a subset of nodes of
        the graph, keys are node ids and values are pairs of x/y
        coordinates
    title : str, optional
        Plot title

    Returns
    -------
    pos : dict
        Dictionary containing positioning of all nodes of
        the graph, keys are node ids and values are pairs of x/y
        coordinates
    """
    pos = None
    fixed = None
    if parent_pos is not None and len(parent_pos) > 0:
        pos = copy.deepcopy(parent_pos)
        fixed = list(parent_pos.keys())

    pos = nx.spring_layout(graph, k=0.9, pos=pos, fixed=fixed)
    # if not parent_pos:

    # else:
    #     pos = copy.deepcopy(parent_pos)
    #     random_pos = nx.spring_layout(graph)
    #     for node in graph.nodes():
    #         if node not in pos:
    #             pos[node] = random_pos[node]

    nx.draw_networkx_nodes(graph, pos, node_color=[[0.6, 0.8, 0.047]] * len(graph.nodes()),
                           node_size=200)
    nx.draw_networkx_edges(graph, pos, alpha=0.4, width=2.0, node_size=200)

    labels = {}
    for node in graph.nodes():
        labels[node] = str(node)

    offset = 0.15
    labels_pos = copy.deepcopy(pos)
    for p in pos:  # raise text positions
        labels_pos[p][1] += offset
    nx.draw_networkx_labels(graph, labels_pos, labels, font_size=11)

    _ticks_off()
    _set_limits(pos, labels_pos)

    if title is not None:
        plt.title(title)

    # save to a file
    if filename is not None:
        plt.savefig(filename)
        plt.clf()
    else:
        plt.show()
    return pos


def plot_instance(graph, pattern, instance, filename=None,
                  parent_pos=None, title=None):
    """Plot the graph with instance of pattern highlighted.

    This util plots a graph and highlights an instance of a pattern
    graph. If `filename` is specified, saves the plot into the file,
    otherwise invokes `matplotlib.pylab.show` function
    (shows the plot). In addition, this function allows to
    specify user defined position for some subset of
    graphs nodes (with `parent_pos` parameter), nodes
    whose positioning is not specified in `parent_pos` are
    placed using `nx.spring_layout` function.

    Parameters
    ----------
    graph : nx.(Di)Graph
        Graph object to plot
    pattern : nx.(Di)Graph
        Graph object representing a pattern graph
    instance : dict
        Dictionary representing an instance of the pattern inside
        of the graph, keys are nodes of the pattern and values are
        corresponding nodes in the graph.
    filename : str, optional
        Path to file to save the plot
    parent_pos : dict
        Dictionary containing positioning of a subset of nodes of
        the graph, keys are node ids and values are pairs of x/y
        coordinates
    title : str, optional
        Plot title

    Returns
    -------
    pos : dict
        Dictionary containing positioning of all nodes of
        the graph, keys are node ids and values are pairs of x/y
        coordinates
    """
    nodes = list(graph.nodes())

    node_color = [0.6, 0.8, 0.047]
    instance_color = [0.788, 0.298, 0.298]
    new_colors = [node_color if not nodes[i] in instance.values()
                  else instance_color for i, c in enumerate(nodes)]

    pos = None
    fixed = None
    if parent_pos is not None and len(parent_pos) > 0:
        pos = copy.deepcopy(parent_pos)
        fixed = list(parent_pos.keys())

    pos = nx.spring_layout(graph, k=0.9, pos=pos, fixed=fixed)

    nx.draw_networkx_nodes(graph, pos, node_color=[node_color] * len(nodes),
                           node_size=200)
    nx.draw_networkx_edges(graph, pos, alpha=0.4, width=2.0, node_size=200)

    # Draw pattern edges highlighted
    edgelist = [(instance[edge[0]], instance[edge[1]])
                for edge in pattern.edges()]
    nx.draw_networkx_edges(
        graph, pos,
        edgelist=edgelist,
        width=3, alpha=0.3, edge_color=[instance_color] * len(edgelist), node_size=200)

    labels = {}
    for node in nodes:
        labels[node] = node
    offset = 0.15
    labels_pos = copy.deepcopy(pos)
    for p in pos:  # raise text positions
        labels_pos[p][1] += offset
    nx.draw_networkx_labels(graph, labels_pos, labels, font_size=11)

    # color the instances

    _ticks_off()
    _set_limits(pos, labels_pos)

    if title is not None:
        plt.title(title)

    if filename is not None:
        with open(filename, "w") as f:
            plt.savefig(f)
            plt.clf()
    else:
        plt.show()
    return


def plot_rule(rule, filename=None, title=None):
    """Plot ReGraph's rule object.

    This function plots a rule object, it produces three
    separate plots: for the left-hand side of the rule,
    preserved part and the right-hand side, where the two
    homomorphsisms p->lhs, p->rhs are encoded with colors
    of nodes.

    Parameters
    ----------
    rule : regraph.rules.Rule
        Rule object to plot
    filename : str, optional
        Path to file to save the plot
    """
    fig = plt.figure(figsize=(14, 3))
    if title is not None:
        st = fig.suptitle(title, fontsize=14)

    # generate colors
    p_colors_dict = {}
    p_colors = []
    for node in rule.p.nodes():
        lhs_node = rule.p_lhs[node]
        all_p_keys = keys_by_value(rule.p_lhs, lhs_node)
        if len(all_p_keys) > 1:
            found = None
            for p_key in all_p_keys:
                if p_key != node and p_key in p_colors_dict.keys():
                    found = p_key
                    break
            if found:
                p_colors_dict[node] = p_colors_dict[found]
                p_colors.append(p_colors_dict[found])
            else:
                p_colors_dict[node] = np.random.rand(3,)
                p_colors.append(p_colors_dict[node])
        else:
            p_colors_dict[node] = np.random.rand(3,)
            p_colors.append(p_colors_dict[node])

    lhs_colors = []
    for node in rule.lhs.nodes():
        p_keys = keys_by_value(rule.p_lhs, node)
        if len(p_keys) > 0:
            lhs_colors.append(p_colors_dict[p_keys[0]])
        else:
            lhs_colors.append(np.random.rand(3,))

    rhs_colors = []
    for node in rule.rhs.nodes():
        p_keys = keys_by_value(rule.p_rhs, node)
        if len(p_keys) > 0:
            rhs_colors.append(p_colors_dict[p_keys[0]])
        else:
            rhs_colors.append(np.random.rand(3,))

    p_pos = nx.spring_layout(rule.p, k=0.7)

    lhs_pos = dict()
    lhs_fixed = []
    for node in rule.lhs.nodes():
        p_keys = keys_by_value(rule.p_lhs, node)
        if len(p_keys) > 0:
            lhs_pos[node] = p_pos[p_keys[0]]
            lhs_fixed.append(node)
    lhs_pos = nx.spring_layout(rule.lhs, pos=lhs_pos, fixed=lhs_fixed, k=0.7)

    rhs_pos = dict()
    rhs_fixed = []
    for node in rule.rhs.nodes():
        p_keys = keys_by_value(rule.p_rhs, node)
        if len(p_keys) > 0:
            rhs_pos[node] = p_pos[p_keys[0]]
            rhs_fixed.append(node)
    rhs_pos = nx.spring_layout(rule.rhs, pos=rhs_pos, fixed=rhs_fixed, k=0.7)

    plt.subplot(1, 3, 1)
    plt.title("LHS")
    _ticks_off()
    nx.draw_networkx_nodes(rule.lhs, lhs_pos,
                           node_color=lhs_colors,
                           node_size=100, arrows=True)
    nx.draw_networkx_edges(rule.lhs, lhs_pos, alpha=0.4, node_size=100)

    labels = {}
    for node in rule.lhs.nodes():
        labels[node] = str(node)
    offset = 0.15
    lhs_label_pos = copy.deepcopy(lhs_pos)
    for p in lhs_pos:  # raise text positions
        lhs_label_pos[p][1] += offset
    nx.draw_networkx_labels(rule.lhs, lhs_label_pos, labels, font_size=11)

    plt.subplot(1, 3, 2)
    plt.title("P")
    _ticks_off()
    nx.draw_networkx_nodes(rule.p, p_pos,
                           node_color=p_colors,
                           node_size=100, arrows=True)
    nx.draw_networkx_edges(rule.p, p_pos, alpha=0.4, node_size=100)

    labels = {}
    for node in rule.p.nodes():
        labels[node] = str(node)
        # if types:
        #     labels[node] += ":" + str(graph.node[node].type_)
    offset = 0.15
    p_label_pos = copy.deepcopy(p_pos)
    for p in p_pos:  # raise text positions
        p_label_pos[p][1] += offset
    nx.draw_networkx_labels(rule.p, p_label_pos, labels, font_size=11)

    plt.subplot(1, 3, 3)
    plt.title("RHS")
    _ticks_off()
    nx.draw_networkx_nodes(rule.rhs, rhs_pos,
                           node_color=rhs_colors,
                           node_size=100, arrows=True)
    nx.draw_networkx_edges(rule.rhs, rhs_pos, alpha=0.4, node_size=100)

    labels = {}
    for node in rule.rhs.nodes():
        labels[node] = str(node)
    offset = 0.15
    rhs_label_pos = copy.deepcopy(rhs_pos)
    for p in rhs_pos:  # raise text positions
        rhs_label_pos[p][1] += offset
    nx.draw_networkx_labels(rule.rhs, rhs_label_pos, labels, font_size=11)

    if title is not None:
        st.set_y(0.95)
        fig.subplots_adjust(top=0.75)

    if filename is not None:
        with open(filename, "w") as f:
            plt.savefig(f)
            plt.clf()
    else:
        plt.show()
    return
