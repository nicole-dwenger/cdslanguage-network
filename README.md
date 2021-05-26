# Network Analysis of Named Entities in Fake and Real News

[Description](#description) | [Methods](#methods) | [Repository Structure](#repository-structure) | [Usage](#usage) | [Results and Disucssion](#results-and-discussion) | [Contact](#contact)

## Description
> This project relates to Assignment 4: Network Analysis of the course Language Analytics.

The aim of this project was to combine the method of Network Analysis and with named entities in text. Specifically, named entities of persons were extracted from a dataset of fake and real news, to investigate their importance and relationships. Rather than only looking at the entire news data, networks were also generated using subsets of fake and real news, to be able to compare the people mentioned in these text documents. Thus, this repository contains two scripts: (1) targeted towards the news data, to extract a weighted edge-list of texts in the fake and real news dataset, and (2) a generalisable command-line script for simple network analysis. When developing the scripts, one aim was also to bundle up functions in a class to increase code modularity.


## Methods

### Data and Preprocessing
The dataset of fake and real news was downloaded from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset), containing 7796 news texts, which are labeled as fake or real. To create the weighted edge-list, this data was preprocessed using the following steps: 

1. Extract named entities of PERSON with spaCy’s model `en_core_web_sm`.
2. Many of the extracted names entities referred to the same person, but were spelled slightly differently or only contained part of the full name. I decided to remove some of the duplicates, but this step is in no way exhaustive and might induce biases (see note below!). The following names were replaced: 
    - Remove ":" (were appearing in some named entities).
    - Replace *Hillary*, *hillary*, *Clinton*, *clinton*, *hillary clinton*, *Hillary Rodham Clinton*, *Hillary Clinton's* with *Hillary Clinton*.
    - Replace *trump*, *Trump*, *donald trump*, *Donald J Trump*, *Donald J. Trump* with *Donald Trump*.
    - Replace *obama*, *Obama*, *barack obama* with *Barack Obama*.
3. Extract all combinations (edges) of pairs of named entities (nodes) within each text. 
4. Calculate the number of occurrences of these combinations (edges) across all texts.
5. Save pairs of nodes and their occurances (weight) in a .csv file, with columns nodeA, nodeB, weight.

**Note:** I am aware, that the replacing of names in step 2 might induce some biases, as these names might have a higher weight, compared to others were variations of names are still present. Ideally, all names referring to the same name could be replaced. However, this also relies on some assumptions, e.g. *Hillary* is *Hillary Clinton* and not a different *Hillary*. 

### Network Analysis
Two important concepts in network analysis are nodes and edges. For this project, the nodes were the extracted named entities of people, while their relations are the edges of the network. The network analysis was performed by generating a network graph of the weighted edgelist. This graph was generated using a spring layout, which positions nodes using the Fuchterman-Reinglod force-directed algorithm (more information [here](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html)). Further, the following centrality measures were extracted, to provide additional information about the nodes and edges. *Degree centrality* is a measure of how many edges are connected to a given node. A node (entity) which is connected to many nodes may be more important. *Eigenvector centrality* is a measure of how much a given node is connected to other well-connected nodes. A node which is connected to other well-connected nodes may also be more important and have higher influence in the network. *Betweenness centrality* is a measure of how important the node is for connections between other nodes. Thus, it may indicate how important the node is for the general flow or interconnectedness of the network.


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
The raw data, which was originally downloaded from [Kaggle](https://www.kaggle.com/nopdev/real-and-fake-news-dataset) is stored in the `data/` directory of this repository. Thus, after cloning the repository, no additional data needs to be retrieved.


### 3. Scripts
This repository contains two scripts: `0_create_edgelist.py` and `1_network_analysis.py`. The former is specifically targeted towards the fake and real news dataset, and processes the data as described above to return a weighted edgelist. The `1_network_analysis.py` script conducts the actual network analysis, and is aimed to be more generalisable, as it can be used with any weighted edgeless stored in a CSV file, with the columns nodeA, nodeB, weight. Detailed instructions to run the scripts is provided below. 
 
### 3.0. Script to preprocess news data: 0_create_edgelist.py
The script 0_create_edgelist.py preprocesses the news dataset, as described in [preprocessing](#data-and-preprocessing). As the news dataset can be divided into fake and real news, it has the option to create edgelists for these subsets of data.  The script should be called from the `src/` directory: 

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
The script `1_network_analysis.py` takes a CSV file with the columns nodeA, nodeB, weight, to generate a network graph with a spring layout, and save centrality measures (degree, eigenvector, betweenness) in a CSV file. The script should be called from the `src/` directory: 

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
    
- `-m, --min_edgeweight`: *int, optional, default:* `500`\
   Minimum edgeweight to consider for network graph. 
   

__Output__ saved in `out/1_network_analysis/`: 

- `network_graph_{input_filename}.png`\
   Network graph of edges with minimum edgeweight, using spring layout. 

- `centrality_measures_{input_filename}.csv`\
   CSV with columns of node, degree, eigenvector, betweenness for centrality measures of edges of nodes with minimum edgeweight. 
  

## Results and Discussion 
Output of the scripts can be found in the corresponding directory in `out/`. Besides providing a script for simple network analysis, the aim of this project was also to compare the networks of named entitie (people) in fake and real news. Below, the networks of fake and real news for edges with a minimum edgeweight of 500 are displayed:

Network graph of real news with minimum edgeweight of 500:

![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network/network_graph_edgelist_REAL.png)

Network graph of fake news with minimum edgeweight of 500:

![](https://github.com/nicole-dwenger/cdslanguage-network/blob/master/out/1_network/network_graph_edgelist_FAKE.png)

Overall, in both graphs Hillary Clinton seems to be an important node in the data, as she also has the highest centrality measures, for degree, eigenvector, betweenness. Further, Donald Trump, Barack Obama and Bill Clinton also seem to be quite interconnected and closely related to Hillary. As mentioned above, replacing variants of names for some people, but not for all might have induced some biases in the data, such that those for which names were summarise have a higher weight, than those where several name variants are still in the data. 

When comparing graphs of real and fake news, it seems like there are fewer nodes and edges in the fake compared to the real news. Looking at the .csv of centrality measures, there is about half (54) as many nodes in the fake compared to the real (98) news data. This could have several reasons, such as overall fewer named entities in the fake news data (which could also be caused by less text), fewer entities which are highly connected (with a minimum edgeweight of 500). 


## Contact
If you have any questions, feel free to contact me at 201805351@post.au.dk.