import pandas as pd
import networkx as nx
import numpy as np

def load_data():
    '''
    This function allows the loading of the network.
    RETURN : 
        - Airport_Network : Networkx graph object corresponding to the network.
    '''
    # The loading of this airport dataset is the first thing done :
    df_airport = pd.read_csv('./openflights/airports.dat.txt', header = None)
    # Rename columns as it should be according to the documentation.
    df_airport = df_airport.rename(columns ={0:'Airport_ID',
                                             1:'Name',
                                             2:'City',
                                             3:'Country',
                                             4:'IATA',
                                             5:'ICAO',
                                             6:'Latitude',
                                             7:'Longitude', 
                                             8:'Altitude',
                                             9:'Timezone', 
                                             10:'DST', 
                                             11:'Tz_database_time',
                                             12:'Type',
                                             13:'Source'})
    
    # Load routes data
    df_routes = pd.read_csv('./openflights/routes.dat.txt', header = None)
    
    # Load the network from the raw data
    # Transform ID into string
    df_airport['Airport_ID'] = df_airport['Airport_ID'].astype(str)
    # Creation of the graph
    Airport_Network=nx.DiGraph()
    # First creation of the nodes
    for i in df_airport.Airport_ID :
        Airport_Network.add_node(str(i))
    # Creation of the edges in a second time
    for i in df_routes.index :
        source_node = df_routes.loc[i][3]
        target_node = df_routes.loc[i][5]
        Airport_Network.add_edge(source_node, target_node) 
    # Add external information
    Airport_Network = add_exogenous_feature(Airport_Network, df_airport)
    
    return Airport_Network
    
    
    
def add_exogenous_feature(G, df_airport):
    '''
    This function allows the addition of external information on each node of the graph given as input.
    ARGS :
        - G : networkx graph object on which external information will be added.
        - df_airport : Pandas dataframe containing the new information to add.
    RETURN : 
        - G : networkx graph object containing new external information on each node.
    '''
    # Add exogenous information
    for i in G.node:
        if df_airport[df_airport.Airport_ID==i].shape[0] != 0:
            G.node[i]['City'] = df_airport[df_airport.Airport_ID==i]['City'].values[0]
            G.node[i]['Country'] = df_airport[df_airport.Airport_ID==i]['Country'].values[0]
            G.node[i]['Latitude'] = df_airport[df_airport.Airport_ID==i]['Latitude'].values[0]
            G.node[i]['Longitude'] = df_airport[df_airport.Airport_ID==i]['Longitude'].values[0]
        else :
            G.node[i]['City'] = np.nan
            G.node[i]['Country'] = np.nan
            G.node[i]['Latitude'] = np.nan
            G.node[i]['Longitude'] = np.nan
    return G

def load_df_airport():
    '''
    This function allows the loading of the dataframe describing the network.
    RETURN : 
        - df_airport : Pandas dataframe describing the network.
    '''
    
    # The loading of this airport dataset is the first thing done :
    df_airport = pd.read_csv('./openflights/airports.dat.txt', header = None)
    # Rename columns as it should be according to the documentation.
    df_airport = df_airport.rename(columns ={0:'Airport_ID',
                                             1:'Name',
                                             2:'City',
                                             3:'Country',
                                             4:'IATA',
                                             5:'ICAO',
                                             6:'Latitude',
                                             7:'Longitude', 
                                             8:'Altitude',
                                             9:'Timezone', 
                                             10:'DST', 
                                             11:'Tz_database_time',
                                             12:'Type',
                                             13:'Source'})
    return df_airport

def weighted_network_creation():
    '''
    This function allows the loading of the weighted network.
    RETURN:
        - Airport_Network_weighted : Networkx graph object representing the graph we want to study
    '''
    df_airport = load_df_airport()
    df_duplicates = pd.read_csv('./openflights/routes.dat.txt', header = None)
    # Rename columns to give meaningful names
    df_duplicates = df_duplicates.rename(columns = {3:'Source_Node', 5:'Target_Node', 7:'Weight'})
    df_duplicates = df_duplicates[['Source_Node', 'Target_Node', 'Weight']]
    # Define a weight of 1 for each node
    df_duplicates['Weight'] = 1
    # Summation of the duplicate edges by storing the sum values in the 'weight' column
    df_weighted = df_duplicates.groupby(['Source_Node', 'Target_Node']).sum().reset_index()
   # Add exogenous information on the weighted version of the graph
    df_airport_tmp = df_airport[['Airport_ID', 'City', 'Country', 'Latitude', 'Longitude']].rename(columns = {'Airport_ID':'Source_Node'} )
    df_airport_tmp['Source_Node'] = df_airport_tmp['Source_Node'].astype(str)
    df_complete = df_weighted.merge(df_airport_tmp, how = 'inner', on = 'Source_Node')
    df_weighted['Source_Node'] = df_weighted['Source_Node'].astype(str)
    df_weighted['Target_Node'] = df_weighted['Target_Node'].astype(str)
    df_airport['Airport_ID'] = df_airport['Airport_ID'].astype(str)
    # Load the network.
    Airport_Network_weighted = nx.from_pandas_edgelist(df_weighted, 'Source_Node', 'Target_Node', edge_attr='Weight', create_using=nx.DiGraph())
    Airport_Network_weighted = add_exogenous_feature(Airport_Network_weighted, df_airport)
    
    return Airport_Network_weighted
