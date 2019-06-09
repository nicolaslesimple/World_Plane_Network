# Our standard ploting module.
import matplotlib.pyplot as plt
# Our standard network analysis module. 
import networkx as nx
import numpy as np
import pandas as pd
import mplleaflet
from load_data import load_df_airport


def plt_directed(G, title):
    '''
    This function allows the visualization of the directed graph given as input in a nice way.
    ARGS :
        - G : nx graph object which is the graph that we want to plot.
        - title : string corresponding to the title of the plot.
    RETURN :
        - None object is return but a plot is printed as output.
    '''
    plt.figure(figsize=(15,10))
    pos = nx.layout.spring_layout(G) # set a layout
    node_sizes = [3 + i/50 for i in range(len(G))] # set different size for each node
    M = G.number_of_edges()
    edge_colors = range(2, M + 2) # set different color for each edge
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes,
                                   arrowsize=1, edge_color=edge_colors,
                                   edge_cmap=plt.cm.Blues, width=0.3)

    ax = plt.gca()
    ax.set_axis_off()
    plt.title(title)
    plt.show()
    
    
def nx_hist(x, bins, normed = False, yscale = 'linear', title = None, xlabel = 'Degree', ylabel = 'Count', cumulative = False):
    '''
    This function can be used for plotting histograms.
    ARGS: 
    - x: The input data (x) should be in the form of a list.
    - Each other input is just a variable determining some characteristic of the resulting plot : 
        - bins: Integer corresponding to the number of bins used in the histogram.
        - normed: Boolean indicating if we want to normalize the histogram.
        - yscale: String which should be 'linear' or 'log' indicating the scale of the y-axis.
        - title: String corresponding to the title of the histogram.
        - xlabel, ylabel: String corresponding to each axis.
    RETURN :
        - This function returns nothing but it plots the wanted histogram. None object is returned.
    NOTE : 
    As this is basically just a wrapper of the matplotlib hist function, its documentation can be consulted as well.    
    '''
    density = None
    if(normed):
        density = 1
        ylabel = 'Probability'
    plt.hist(x, bins=bins, normed=density, cumulative = cumulative)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yscale(yscale)
    plt.title(title)
    plt.grid(True)
    plt.show()
    
def ScatterPlot(X_Variable,X_VariableName,Y_Variable,Y_VariableName):
    '''
    This function allows the making of pretty scatter plots.
    ARG :
        - X_variable : List corresponding to the different values of the X_varaibale of the scatter plot.
        - X_VariableName : String corresponding to the name of the X variable we will use in the label of the plot.
        - Y_variable : List corresponding to the different values of the Y_varaibale of the scatter plot.
        - Y_VariableName : String corresponding to the name of the Y variable we will use in the label of the plot.
    RETURN :
        - None object is return but a scatter plot and some correlation values are printed. 
    '''
    # Scatter plot
    fig = plt.figure(figsize = (10, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel(X_VariableName,fontsize=10)
    ax.set_ylabel(Y_VariableName,fontsize=10)
    plt.scatter(X_Variable, Y_Variable, alpha=0.5)
    plt.title(f'Scatter plot of the {Y_VariableName} in function of {X_VariableName} coming from the Airport_Network')
    plt.xlim(left=-0.001)
    plt.ylim(bottom=-0.001)
    plt.show()
    # Correlation coefficient 
    df = pd.DataFrame()
    df[X_VariableName] = X_Variable
    df[Y_VariableName] = Y_Variable
    method = ['pearson', 'spearman']
    print(f'The Pearson Correlation coefficient (linear) for these two variable is {df.corr(method=method[0])[X_VariableName][Y_VariableName]}')
    print(f'The Spearman Correlation coefficient (monotonic) for these two variable is {df.corr(method=method[1])[X_VariableName][Y_VariableName]}')
    
def Geographical_visualization(G, list_country = None):
    '''
    This function allows a geographical visualization of the network using mpleaflet library.
    ARGS :
        - G : Networkx Graph that we want to visualize. Each node should have longitude and latitude attribute.
        - list_country = List of string corresponding of the name of the country we want to analyse : it restricts the area.
    RETURN :
        - None object is return but a new windows is opened with a interactive visualization.
    '''
    if list_country == None :
        G_plot = G.copy()
        G_plot = G_plot.to_undirected()
        pos={}
        # We remove node from our graph which have no longitude or latitude values
        for i in G.nodes:
            if (type(G.node[i]['Longitude'])!=np.float64)&(type(G.node[i]['Latitude'])!=np.float64):
                G_plot.remove_node(i)
            if (type(G.node[i]['Longitude'])==np.float64)&(type(G.node[i]['Latitude'])==np.float64):
                pos[i] = [G.node[i]['Longitude'],G.node[i]['Latitude']]
        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(G_plot,pos=pos,node_size=10,node_color='red',edge_color='k',alpha=.5, with_labels=False)
        nx.draw_networkx_edges(G_plot,pos=pos,edge_color='gray', alpha=.1)
        nx.draw_networkx_labels(G_plot,pos, label_pos =10.3)
        mplleaflet.show()
    
    else :
        
        df_airport = load_df_airport()
        df_europe = df_airport[df_airport.Country.isin(list_country)]
        G_plot = G.copy()
        G_plot = G_plot.to_undirected()
        pos={}
        # We remove node from our graph which have no longitude or latitude values
        for i in G.nodes:
            if (type(G.node[i]['Longitude'])!=np.float64)|(type(G.node[i]['Latitude'])!=np.float64)|((G.node[i]['Country'] in list_country)==False):
                G_plot.remove_node(i)
            if (type(G.node[i]['Longitude'])==np.float64)&(type(G.node[i]['Latitude'])==np.float64)&((G.node[i]['Country'] in list_country)==True):
                pos[i] = [G.node[i]['Longitude'],G.node[i]['Latitude']]
        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(G_plot,pos=pos,node_size=10,node_color='red',edge_color='k',alpha=.5, with_labels=False)
        nx.draw_networkx_edges(G_plot,pos=pos,edge_color='gray', alpha=.1)
        nx.draw_networkx_labels(G_plot,pos, label_pos =10.3)
        mplleaflet.show()
        
    
    