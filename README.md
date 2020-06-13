# Page Rank

- Project 3 of Big Data subject
- Implemented by:
   - Theodoros Mandilaras
   - cs2.190018
- MSc DI/EKPA 2019-2020

---

Implementation and evaluation of two different PageRank algorithms on the **Google-web** dataset.

## Algorithm 1

### Simple PageRank equation

``p = M⋅p``

where **p** is a vector of size Nx1 (where N is the number of nodes in the graph). **p[i,1]** represents the
PageRank of page **i**. Initially every page’s PageRank is equal to 1. We repeat the above computation,
i.e., multiplying **M** with **p** and storing in **p** for a pre-specified number of steps.

## Algorithm 2

### Improved version of PageRank

``p = α⋅M⋅p + (1-α)⋅I​n``

where **α** is a numeric value, **N** is the number of pages (nodes) in the Web graph, and **In**​ is a unary
vector (i.e., all values are set to 1) of size Nx1.

---

## About Implementation

The program can be executed in three different modes:

### Default Mode
In the default mode, the program gets from the arguments the desired method, the path for the graph and the number of 
the iterations (is improved method has been selected, it also get the `a` numeric value). Then, performs the selected 
algorithm for the desired number of iterations. 
**Output**: In the end, it stores the top and bottom 20 in a txt file in the results directory, and also it makes the 
histogram for the current ranks.

### Evaluate Mode:
The evaluate mode implemented to executed and store the outputs for all the requested iterations (10, 50, 100, 200) 
with a single run. 

### Converge Mode:
In this mode the selected algorithm iterates util the sum of the absolute differences between last rank vector and the 
new one is less than a `e` value.

### Results structure
The program create a directory for the results. inside it created three folders:
- results: In this folder the top and bottom 20 csv are stored. Files format: 
`<method>_<a value>_<iterations>_<bottom20 or top20>.txt`
- plots: In this folder the histogram plots are stored. Files format: `<method>_<a value>_<iterations>.png`
- ranks: That was a folder for development help. It is no more used.

---

## How to run?

The program makes use of the Argparse module to parse the arguments. 
The required arguments are:

- `-p` or `--path`: the path for the .txt file with the graph
- `-m` or `--method`: to set the selected method. Options are 'simple', 'improved'

Optional arguments:
- `-i` or `--iterations`: to set how many iterations the program to perform. 
- `-a` or `--a`: The numeric value used for the improved algorithm
- `-c` or `--converge`: To enable the mode with the convergence
- `-e` or `--eval`: To execute the evaluate mode.

### Example:
Simple execution for the default mode with the simple algorithm for 100 iterations:
`python page_ranking.py -m simple -p web-Google.txt -i 100`

Similarly for the improved algorithm
`python page_ranking.py -m improved -p web-Google.txt -i 100`

Evaluate mode:
`python page_ranking.py -m improved -p web-Google.txt -e`

Convergence mode. If iterations mentioned, they will
be ignored.
  
`python page_ranking.py -m simple -p web-Google.txt -c`



