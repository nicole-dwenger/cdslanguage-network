# Assignment 4: Network Analysis

[Description](#description) | [Methods](#methods) | [Repository Structure](#repository-structure) | [Usage](#usage) | [Results and Disucssion](#results-and-discussion)

## Description
> This project relates to Assignment 3: Network Analysis of the course Language Analytics.

Additional:
- Attempt to implement coreference resolution on entities (time-consuming)
- Bundle your code up into a Python class, focusing on code modularity
- Let the user define which graphing algorithm they use (pretty tricky)
- Are there other ways of creating networks, rather than just document co-occurrence? (really tricky)

Network Analysis ..


Can be used to find entities, which are occuring together in the same document. 
The aim of this project was to build a reusable command-line tool to perform a simple network analysis. The data used for this project was dataset of real and fake news from kaggle. Thus, this script contains both a script to extract a weighted edgelist of this particular dataset, and a rather generalisable script to conduct a simple network analysis of a preprocessed, weighted edgelist. Further, this project aims to illustrate how functions for the network analysis can be bundled up into a class. 

## Methods

### Data and Preprocessing
The data used for this project is a dataset from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset), containing 7796 news texts, which are labeled as *FAKE* or *REAL*. For the network analysis, this data was preprocessed to extract a weighted edgelist, using the following steps: 

1. Extract named entities of each text
2. Clean the named entities (this step is not exhaustive!):
    - Remove ":" (were appearing in some named entities)
    - Replace "Hillary", "hillary", "Clinton", "clinton", "hillary clinton", "Hillary Rodham Clinton", "Hillary Clinton's" with "Hillary Clinton"
    - Replace "trump", "Trump", "donald trump" with "Donald Trump"
    - Replace "obama", "Obama", "barack obama" with "Barack Obama"
3. Generate all possible combinations (edges) of pairs of named entities (nodes) 
4. Calculate the number of occurance of these combinations (edges) 
5. Save pairs of nodes and their occurance (weight) in a dataframe, with `nodeA`, `nodeB`, `weight`

### Network Analysis


Centrality measures, can provide information about the nodes (i.e. in this case the people). Degree centrality is a measure of how many edges are connected to a given node:
- Degree centrality: measure of how many edges are connected to a given node
- Eigenvector centraliy: measure of how much a given node is connected to other well-connected nodes
- Betweenness centrality: measure of how import the node is for connections between other nodes, i.e. the flow of the network


## Repository Structure 
```
|-- data/
    |-- fake_or_real_news.csv                        # Raw data of fake and real news texts
    
|-- out/                                             # Directory for output, corresponding to scripts
    |-- 0_edgelists/                                 # Output of 0_create_edgelist.py
        |-- edgelist_FAKE.csv                        # Preprocessed, weighted edgelist for FAKE news
        |-- edgelist_REAL.csv                        # Preprocessed, weighted edgelist for FAKE news
        |-- edgelist_ALL.csv                         # Preprocessed, weighted edgelist for ALL news
    |-- 1_network_analysis/                          # Output of 1_network_analysis.py 
        |-- network_graph_edgelist_FAKE.png          # Visualisation of network for fake news
        |-- network_graph_edgelist_REAL.png          # Visualisation of network for real news
        |-- centrality_measures_edgelist_FAKE.csv    # Centrality measures of fake news 
        |-- ...                      

|-- src/
    |-- 0_create_edgelist.py             # Script for preprocessing: creating edgelist of news dataset
    |-- 1_network_analysis.py            # Script for network analysis: graphing and centrality measures
    
|-- README.md
|-- create_venv.sh                       # Bash script to create virtual environment
|-- requirements.txt                     # Dependencies, installed in virtual environment

```

## Usage 
**!** The scripts have only been tested on Linux, using Python 3.6.9. 

### 1. Cloning the Repository and Installing Dependencies
To run the scripts in this repository, I recommend cloning this repository and installing necessary dependencies in a virtual environment. The bash script `create_venv.sh` can be used to create a virtual environment called `venv_network` with all necessary dependencies, listed in the `requirements.txt` file. The following commands can be used:

```bash
# cloning the repository
git clone https://github.com/nicole-dwenger/cdslanguage-network.git

# move into directory
cd cdslanguage-network/

# install virtual environment
bash create_venv.sh

# activate virtual environment 
source venv_network/bin/activate
```

### 2. Data 
The raw data, which was originally downloaded from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset) is stored in the `data/` directory of this repository. Thus, when the repository is cloned, no additional data needs to be retrieved. 
The `0_create_edgelist` script is specifically targeted towards this dataset. However, the `1_network_analysis.py` script can be used with any .csv file, with the columns `nodeA, nodeB, weight`. 


### 3.0. Script to preprocess news data: 0_create_edgelist.py
The script `0_create_edgelist.py` preprocesses the news dataset, as described in [preprocessing](#data-and-preprocessing). The script should be called from the `src/` directory: 

```bash
# move into src 
cd src/

# run script with default parameters
python3 0_create_edgelist.py

# run script for specified input data
python3 0_create_edgelist.py -s REAL
```

__Parameters:__

- `-i, --input_filepath`: *str, optional, default:* `../data/fake_or_real_news.csv`\
    File path to data. The script is targeted towards the real and fake news dataset.
    
- `-s, --subset_input`: *str, optional, default:* `ALL`\
   Subset of news to consider when creating edgelist, should be `ALL`, `REAL` or `FAKE`.
   

__Output__ saved in `out/0_edgelists/`: 

- `edgelist_{subset_input}.csv`\
  CSV file of weighted edgelist with columns of `nodeA, nodeB, weight`. 


### 3.1. Script for network analysis: 1_network_analysis.py
The script `1_network_analysis.py` takes a csv file with `nodeA, nodeB, weight`, to generate a network graph with a spring layout, and save centrality measures (degree, eigenvector, betweenness) in a csv file. The script should be called from the `src/` directory: 

```bash
# move into src 
cd src/

# run script with default parameters
python3 1_network_analysis.py

# run script for specified input data
python3 0_create_edgelist.py -i ../out/0_edgelists/edgelist_FAKE.csv
```

__Parameters:__

- `-i, --input_filepath`: *str, optional, default:* `../out/0_edgelists/edgelist_REAL.csv`\
    File path to csv of weighted edgelist with with columns `nodeA, nodeB, weight`. If you have preprocessed the fake and real news dataset and which to run network analysis for these files, use default for REAL, `../out/0_edgelists/edgelist_FAKE.csv` or `../out/0_edgelists/edgelist_ALL.csv`
    
- `-m, --min_edgeweight`: *str, optional, default:* `500`\
   Minimum edgeweight to consider for network graph. 
   

__Output__ saved in `out/0_network_analysis/`: 

- `network_graph_{input_filename}.png`\
   Network graph of edges with minimum edgeweight, using spring layout. 

- `centrality_measures_{input_filename}.csv`\
   CSV with columns of `node, degree, eigenvector, betweenness` for centrality measures of edges of nodes 
   with minimum edgeweight. 
  

## Results and Discussion 
Output of the scripts can be found in the corresponding directory in `out/`. Besides providing a script for simple network analysis, the aim of this project was also to compare the networks of persons mentioned in fake and real news. Below, the networks of fake and real news for edges with a minimum edgeweight of 500 are displayed.

REAL news: 
![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network_analysis/centrality_measures_edgelist_REAL.csv)

FAKE news:
![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network_analysis/centrality_measures_edgelist_FAKE.csv)












