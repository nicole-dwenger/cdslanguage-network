#!/usr/bin/env python

"""
This script preprocesses data for network analysis. 
It extract named entities of PERSON across texts, and creates a weighted edgelist. 

Steps:
  - Save all texts in a list
  - Extract named entities for each text
  - Create a list of edges (co-occurence of named entities) for all texts
  - Count how often each edge occurs across texts
  - Save weighted edgelist in df with "nodeA", "nodeB", "weight"

Input: 
  - -i, --input_filepath, str, optional, default: ../data/fake_or_real_news.csv, path to csv file to be preprocessed
  - -s, --subset_option, str, optional, default: REAL, should be either  "FAKE", "REAL" or "ALL" 
  
Output: 
  - edgelist_{subset}.csv: file with weighted edgelist, with columns "nodeA", "nodeB", "weight"

"""

# LIBRARIES ---------------------------------------------------

# Basics
import os
from tqdm import tqdm 
import argparse
import pandas as pd 
import re

# NLP
import spacy
nlp = spacy.load("en_core_web_sm")

# Edgelist tools
from itertools import combinations
from collections import Counter


# HELPER FUNCTIONS --------------------------------------------
        
def extract_entities(text, label):
    """
    From a text document, extract all named entities and save in list
      - text: text document
      - label: type of named entitiy to extract 
    Returns:
      - entities: list of named enities for text document
    """
    # Create empty target list
    entities = []
    # Apply spacy nlp model
    doc = nlp(text)
    # For each entitiy in the document
    for entitiy in doc.ents:
        # If the entitiy is the given label
        if entitiy.label_ == label:
            # Append the entity text to the list
            entities.append(entitiy.text)
    
    return entities

def clean_entities(raw_entities):
    """
    Function specifically target towards news data,
    remove ":", replace duplicates for Hillary Clinton, Donald Trump, Barack Obama
    Input:
      - raw_entities: list of extracted entities
    Retuns:
      - cleaned_entities: list of cleaned entities
    """
    # remove ":"
    cleaned_entities = [re.sub(r"\:", "", entity) for entity in raw_entities]
    
    # Replace duplicates
    for index, entity in enumerate(cleaned_entities):
        
        # If entity in list, replace with "Hillary Clinton"
        if entity in ["Hillary", "hillary", "Clinton", "clinton", "hillary clinton", 
                      "Hillary Rodham Clinton", "Hillary Clinton's", "Hillary Clinton’s"]:
            cleaned_entities[index] = "Hillary Clinton"
        
        # If entity in list, replace with "Donald Trump"
        if entity in ["trump", "Trump", "donald trump", "Donald J Trump", "Donald J. Trump"]:
            cleaned_entities[index] = "Donald Trump"
        
        # If entity in list, replace with "Barack Obama"
        if entity in ["obama", "Obama", "barack obama"]:
            cleaned_entities[index] = "Barack Obama"
            
    return cleaned_entities
                              
def create_edgelist(cleaned_entities):
    """
    For a given list of entities, create possible combinations, 
    sort combinations to avoid duplicates
    Input: 
      - cleaned_entities: list of cleaned entities, extracted from text
    Output:
      - edgelist: list of all sorted edges in a text
    """
    # Create empty list for edges
    edges = []
    # Create unsorted list of all combinations of entities 
    unsorted_edges = list(combinations(cleaned_entities, 2))
    # Sort each edge in the unsorted edges
    edges = [tuple(sorted(edge)) for edge in unsorted_edges]
    
    return edges
   
def count_edges(edgelist):
    """
    Count occurance of edges in an edgelist, and append to dataframe
    Input:
      - edgelist: list of sorted edges
    Output: 
      - df: df with "nodeA", "nodeB", "weight"
    """
    # Create empty lists for nodes and weights
    nodeA = []
    nodeB = []
    weight = []

    # For each edge and value when counting edges in the edgelist
    for unique_edge, value in Counter(edgelist).items():
        nodeA.append(unique_edge[0])
        nodeB.append(unique_edge[1])
        weight.append(value)
        
    # Save everything in dataframe
    df = pd.DataFrame(zip(nodeA, nodeB, weight), columns = ["nodeA", "nodeB", "weight"])
        
    return df


# MAIN FUNCTION -----------------------------------------------

def main():
    
    # --- ARGUMENT PARSER ---
    
    # Initialise argument parser
    ap = argparse.ArgumentParser()
    
    # Input option for input file
    ap.add_argument("-i", "--input_filepath", help = "Path to input .csv file",
                    required = False, default = "../data/fake_or_real_news.csv")
    
    # Input option for input file
    ap.add_argument("-s", "--subset_option", help = "'FAKE', 'REAL' or 'ALL' news",
                    required = False, default = "REAL")

    # Retrieve input 
    args = vars(ap.parse_args())
    input_filepath = args["input_filepath"]
    subset_option = args["subset_option"]
    
    # --- CREATE EDGELIST ---
    
    # Print message
    print(f"[INFO] Creating weighted edgelist for {input_filepath} for {subset_option} news.")
    
    # Read input csv file
    df = pd.read_csv(input_filepath)
    
    # If subset option is FAKE or REAL, subset dataframe
    if subset_option != "ALL":
        df = df[df["label"] == subset_option]
    
    # Save all texts to a list
    text_list = df["text"].tolist()
    
    # Create empty target edgelist
    edgelist = []
    
    # For each text in the text list
    for text in tqdm(text_list):
        # Extract the entities with the label "PERSON"
        text_entities = extract_entities(text, label="PERSON")
        # Clean entities, i.e. remove duplicates
        cleaned_entities = clean_entities(text_entities)
        # Create an edgelist of the entities, i.e. combinations of nodes
        text_edgelist = create_edgelist(cleaned_entities)
        # Append the text edgelist, to an overall edgelist
        edgelist.extend(text_edgelist)
        
    # Count the number of times each edge occurs in the edgelist and save to df
    edges_df = count_edges(edgelist)
    
    # --- OUTPUT ---
    
    # Prepare output directory
    out_directory = os.path.join("..", "out", "0_edgelists")
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
        
    # Define output path
    out_path = os.path.join(out_directory, f"edgelist_{subset_option}.csv")
    # Save dataframe to csv
    edges_df.to_csv(out_path)
          
    # Print message
    print(f"[INFO] Done! Weighted edgelist saved as csv file in {out_path}")
    
if __name__ == "__main__":
    main()
    