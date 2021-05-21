#!/usr/bin/env python

"""
Script to generate graph and csv of centrality measures from weighted edgelist (csv with nodeA, nodeB, weight)

Steps:
  - Read weighted edgelist and filter by minimum weight
  - Create and save network graph
  - Extract degree, betweenness and eigenvector centrality measures and save as csv

Input: 
  - -i, --input_filepath, optional, default = ../out/0_edgelists/weighted_edgelist_ALL.csv"
  - -m, --minimum_edgeweight, optional, default = 500, mimimum edgeweight to consider for network 
  
Output saved in ../out/1_network_analysis/
  - network_graph_{filename}.py
  - centrality_measures_{filename}.py
"""


# LIBRARIES ---------------------------------------------------

# Basics
import os
import argparse
import pandas as pd

# Network
import math
import networkx as nx
import matplotlib.pyplot as plt


# HELPER FUNCTIONS --------------------------------------------
    
def get_filename(filepath):
    """
    Get filename from filepath, without extension 
    Input:
      - filepath
    Returns:
      - filename: name without directory and entension
    """
    # Get only the name of the file
    filename_ext = os.path.basename(filepath)
    # Get the name of the file without the extnesion
    filename = os.path.splitext(filename_ext)[0]

    return filename
      
    
class NetworkAnalysis:
    
    def __init__(self, edges_df):
        
        # Dataframe with weighted edgelist
        self.edges_df = edges_df
        # Generate graph from edgelist when initialising 
        self.graph = nx.from_pandas_edgelist(self.edges_df, "nodeA", "nodeB", ["weight"])
    
    def draw_graph(self, output_path):
        """
        Draw spring network graph from weighted edgelist and save in output_path as .png
        Input:
          - output_path: outuput_path for graph visualisation
        Appends graph to 
        """
        # Define layout for network, with increased distance between nodes
        spring_layout = nx.spring_layout(self.graph, k=math.sqrt(self.graph.order()))

        # Draw network nodes
        nx.draw_networkx_nodes(self.graph, spring_layout, node_size=10, node_color="steelblue", alpha=0.7)
        # Draw network edges
        nx.draw_networkx_edges(self.graph, spring_layout, width=0.5, alpha=0.3)
        # Draw network labels
        nx.draw_networkx_labels(self.graph, spring_layout, font_size=5, verticalalignment="bottom")

        # Save the graph
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    
    def get_centrality_measures(self, output_path):
        """
        Generate centrality measures from graph and save as dataframe 
        Calcualtes degree, betweenness, eigenvector for each node
        Input: 
          - output_path: output path for csv file
        """
        # Retrieve nodes from graph
        nodes = nx.nodes(self.graph)
        # Retrieve dregree measure from graph
        degree = nx.degree_centrality(self.graph)
        # Retrieve betweenness measure from graph
        betweenness = nx.betweenness_centrality(self.graph)
        # Retrieve eigenvector measure from graph
        eigenvector = nx.eigenvector_centrality(self.graph)

        # Zip nodes and measures together
        centrality_measures = zip(nodes, degree.values(), betweenness.values(), eigenvector.values())
        # Save zipped measures in data frame
        centrality_df = pd.DataFrame(centrality_measures, columns = ["node", "degree", "betweenness", "eigenvector"])
        # Sort dataframe, with highest measures at top
        centrality_df_sorted = centrality_df.sort_values(["degree", "betweenness", "eigenvector"], ascending=False)

        # Save df as csv in output path
        centrality_df_sorted.to_csv(output_path)


# MAIN FUNCTION -----------------------------------------------

def main():
    
    # --- ARGUMENT PARSER AND OUTPUT DIRECTORY ---
        
    # Initialise argument parser
    ap = argparse.ArgumentParser()
    
    # Input option for input file 
    ap.add_argument("-i", "--input_filepath", help="Path to input file, CSV with 'nodeA', 'nodeB', 'weight'",
                    required=False, default="../out/edgelist_ALL.csv")
    
    # Input option for minimum edgeweight to plot
    ap.add_argument("-m", "--min_edgeweight", type=int, help="Minimum edgeweight of interest",
                    required=False, default=500)
    
    # Retrieve inputs
    args = vars(ap.parse_args())
    input_filepath = args["input_filepath"]
    min_edgeweight = args["min_edgeweight"]
        
    # Get name of input file to save corresponding output
    filename = get_filename(input_filepath)
    
    # Create output directory
    out_directory = os.path.join("..", "out", "1_network")
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
        
    # --- NETWORK ANALYSIS ---
    
    print(f"\nInitialising Network Analysis for {input_filepath}.")
    
    # Read edges dataframe
    input_df = pd.read_csv(input_filepath)
    # Keep only those edges which are above the minimum edgeweight 
    edges_df = input_df[input_df["weight"] > min_edgeweight]
    
    # Initialise Network Analysis
    network = NetworkAnalysis(edges_df)
    
    # Create and save network graph
    out_graph = os.path.join(out_directory, f"network_graph_{filename}.png")
    network.draw_graph(out_graph)
    
    # Generate and save centrality measures
    out_measures = os.path.join(out_directory, f"centrality_measures_{filename}.csv")
    network.get_centrality_measures(out_measures)
    
    print(f"Done! Graph and centrality measures saved in {out_directory}")

        
if __name__ == "__main__":
    main()
     