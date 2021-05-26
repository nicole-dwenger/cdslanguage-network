# Assignment 4: Network Analysis

[Description](#description) | [Methods](#methods) | [Repository Structure](#repository-structure) | [Usage](#usage) | [Results and Disucssion](#results-and-discussion) | [Contact](#contact)

## Description
> This project relates to Assignment 4: Network Analysis of the course Language Analytics.

Network Analysis can be applied in many different ways and for different purposes across different fields of research. One of these fields is NLP. For instance, it can be used to find named entities which are occurring in the same document, and thus entities (nodes) and their relations (edges) in a given network. In this project, networks of names entities of people in fake and real news are explored using a dataset from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset). Network graphs and measures are generated for both subsets of real news, fake news, and for all news.

The repository provides two scripts: (1) a script targeted toward the news-headline data, to extract a weighted edge-list of texts in the fake and real news dataset, and (2) a generalisable command-line script for simple network analysis. When developing the scripts, one aim was also to bundle up functions in a class for increased code modularity.

## Methods

### Data and Preprocessing
The data used for this project is a dataset from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset), containing 7796 news texts, which are labeled as FAKE or REAL. For the network analysis, this data was preprocessed to extract a weighted edgelist, using the following steps: 

1. Extract named entities of each text
2. Clean the named entities (this step is not exhaustive!):
    - Remove ":" (were appearing in some named entities).
    - Replace *Hillary*, *hillary*, *Clinton*, *clinton*, *hillary clinton*, *Hillary Rodham Clinton*, *Hillary Clinton's* with *Hillary Clinton*.
    - Replace *trump*, *Trump*, *donald trump*, *Donald J Trump*, *Donald J. Trump* with *Donald Trump*.
    - Replace *obama*, *Obama*, *barack obama* with *Barack Obama*.
3. Generate all possible combinations (edges) of pairs of named entities (nodes). 
4. Calculate the number of occurance of these combinations (edges).
5. Save pairs of nodes and their occurances (weight) in a .csv file, with columns nodeA, nodeB, weight.

**Note:** I am aware, that the replacing of names in step 2 might induce some biases, as these names might have a higher weight, compared to others were variations of names are still present. Ideally, all names referring to the same name could be replaced. However, this also relies on some assumptions, e.g. *Hillary* is *Hillary Clinton* and not a different *Hillary*. 

### Network Analysis
Network Analysis was performed by generating a network graph from the weighted edge-list. This graph was generated using a spring layout, which positions nodes using the Fuchterman-Reinglod force-directed algorithm (more information [here](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html)). Further, it computes centrality measures, which can provide differen information of the nodes (here the named entities, persons) and edges:
- Degree centrality: Degree centrality is a measure of how many edges are connected to a given node. A node (entity) which is connected to many nodes may be more important. 
- Eigenvector centrality: Eigenvector centrality is a measure of how much a given node is connected to other well-connected nodes. A node which is connected to other well-connected nodes may also be more important and have higher influence in the network. 
- Betweenness centrality: Betweenness centrality is a measure of how important the node is for connections between other nodes. Thus, it may indicate how important the node is for the general flow or interconnectedness of the network.


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
The raw data, which was originally downloaded from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset) is stored in the `data/` directory of this repository. Thus, after cloning the repository, no additional data needs to be retrieved. The `0_create_edgelist.py` script is specifically targeted towards this dataset. However, the `1_network_analysis.py` script can be used with any weighted edgeless stored in a .csv file, with the columns nodeA, nodeB, weight. 


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
    
- `-s, --subset_input`: *str, optional, default:* `REAL`\
   Subset of news to consider when creating edgelist, should be `ALL`, `REAL` or `FAKE`.
   

__Output__ saved in `out/0_edgelists/`: 

- `edgelist_{subset_input}.csv`\
  CSV file of weighted edgelist with columns of nodeA, nodeB, weight. 


### 3.1. Script for network analysis: 1_network_analysis.py
The script `1_network_analysis.py` takes a .csv file with the columns nodeA, nodeB, weight, to generate a network graph with a spring layout, and save centrality measures (degree, eigenvector, betweenness) in a csv file. The script should be called from the `src/` directory: 

```bash
# move into src 
cd src/

# run script with default parameters
python3 1_network_analysis.py

# run script for specified input data
python3 1_network_analysis.py -i ../out/0_edgelists/edgelist_FAKE.csv
```

__Parameters:__

- `-i, --input_filepath`: *str, optional, default:* `../out/0_edgelists/edgelist_REAL.csv`\
    File path to csv of weighted edgelist with with columns nodeA, nodeB, weight. If you have preprocessed the fake and real news dataset and which to run network analysis for these files, use default for real news, `../out/0_edgelists/edgelist_FAKE.csv` for fake news or `../out/0_edgelists/edgelist_ALL.csv` for all news.
    
- `-m, --min_edgeweight`: *str, optional, default:* `500`\
   Minimum edgeweight to consider for network graph. 
   

__Output__ saved in `out/1_network_analysis/`: 

- `network_graph_{input_filename}.png`\
   Network graph of edges with minimum edgeweight, using spring layout. 

- `centrality_measures_{input_filename}.csv`\
   CSV with columns of `node`, `degree`, `eigenvector`, `betweenness` for centrality measures of edges of nodes with minimum edgeweight. 
  

## Results and Discussion 
Output of the scripts can be found in the corresponding directory in `out/`. Besides providing a script for simple network analysis, the aim of this project was also to compare the networks of named entitie (people) in fake and real news. Below, the networks of fake and real news for edges with a minimum edgeweight of 500 are displayed:

Network Graph of real news with minimum edgeweight of 500:

![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network/network_graph_edgelist_REAL.png)

Network Graph of fake news with minimum edgeweight of 500:

![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network/network_graph_edgelist_FAKE.png)

Overall, in both graphs Hillary Clinton seems to be an important node in the data, as she also has the highest centrality measures, for degree, eigenvector, betweenness. Further, Donald Trump, Barack Obama and Bill Clinton also seem to be quite interconnected and closely related to Hillary. As mentioned above, replacing variants of names for some people, but not for all might have induced some biases in the data, such that those for which names were summarise have a higher weight, than those where several name variants are still in the data. 

When comparing graphs of real and fake news, it seems like there are fewer nodes and edges in the fake compared to the real news. Looking at the .csv of centrality measures, there is about half (34) as many nodes in the fake compared to the real (98) news data. This could have several reasons, such as overall fewer named entities in the fake news data (which could also be caused by less text), fewer entities which are highly connected (with a minimum edgeweight of 500). 


## Contact
If you have any questions, feel free to contact me at 201805351@post.au.dk.