#!/usr/bin/env python


"""
Script to generate graph and csv of centrality measures from weighted edgelist (csv with nodeA, nodeB, weight)

Steps:
  - Read weighted edgelist and filter by minimum weight
  - Create and save network graph
  - Extract degree, betweenness and eigenvector centrality measures and save as csv

Input: 
  - -i, --input_filepath, required, filepath to edgelist 
  - -m, --minimum_edgeweight, optional, defualt = 500, mimimum edgeweight to consider for network 
  
Output saved in ../out/1_
  - 

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


# MAIN FUNCTION -----------------------------------------------

def main():
    
    # --- ARGUMENT PARSER ---
        
    # Initialise argument parser
    ap = argparse.ArgumentParser()
    
    # Input option for input file 
    ap.add_argument("-i", "--input_filepath", help="Path to input file, CSV with 'nodeA', 'nodeB', 'weight'",
                    required=False, default="../out/weighted_edgelist_FAKE.csv")
    
    # Input option for minimum edgeweight to plot
    ap.add_argument("-w", "--min_edgeweight", type=int, help="Minimum edgeweight of interest",
                    required=False, default=500)
    
    # Retrieve inputs
    args = vars(ap.parse_args())
    input_filepath = args["input_filepath"]
    min_edgeweight = args["min_edgeweight"]
        
    # Create output directory
    out_directory = os.path.join("..")
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
        
    # --- NETWORK ANALYSIS ---
    
    print("START")
    
    # Read edges dataframe
    input_df = pd.read_csv(input_filepath)
    
    # Keep only those edges which are above the minimum edgeweight 
    edges_df = input_df[input_df["weight"] > min_edgeweight]
    
    # Initialise Network Analysis
    network = NetworkAnalysis(edges_df)
    
    # Draw and save draw
    out_graph = os.path.join(out_directory, "graph_test.png")
    network.draw_graph(out_graph)
    
    # Get and save centrality measures
    out_df = os.path.join(out_directory, "df.csv")
    network.get_centrality_measures(out_df)
    
    print("DONE!")
    
      
class NetworkAnalysis:
    
    def __init__(self, edges_df):
        
        self.edges_df = edges_df
        self.graph = None
    
    def draw_graph(self, output_path):
        
        # Draw graph from edgelist
        self.graph = nx.from_pandas_edgelist(self.edges_df, "nodeA", "nodeB", ["weight"])

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
        
        nodes = nx.nodes(self.graph)
        degree = nx.degree_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph)
        eigenvector = nx.eigenvector_centrality(self.graph)

        centrality_measures = zip(nodes, degree.values(), betweenness.values(), eigenvector.values())
        centrality_df = pd.DataFrame(centrality_measures, columns = ["node", "degree", "betweenness", "eigenvector"])
        centrality_df_sorted = centrality_df.sort_values(["degree", "betweenness", "eigenvector"], ascending=False)

        centrality_df_sorted.to_csv(output_path)

        
if __name__ == "__main__":
    main()
     