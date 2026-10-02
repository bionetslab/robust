# New ROBUST version

We have developed a new version of ROBUST which corrects for study bias in PPI networks. The new version is available here: https://github.com/bionetslab/robust_bias_aware. Although this version is still fully functional, we recommend using the latest ROBUST version for your research.

# Installation

## With conda (Bioconda)
```bash
conda install -c conda-forge -c bioconda robust-pcst
```

## With pip
```bash
pip install git+https://github.com/bionetslab/robust.git
```

## From source
To run the script directly from a clone of this repository, install the dependencies (Python >= 3.8) as follows:
```bash
conda create --name robust -c conda-forge -c bioconda python numpy matplotlib pandas networkx pcst-fast
conda activate robust
```

# Running ROBUST

If ROBUST was installed with conda or pip, you can run it by calling
```bash
robust-pcst data/human_annotated_PPIs_brain.txt data/ms_seeds.txt ms.graphml 0.25 0.9 30 0.1
```
From a clone of this repository, you can also call the script directly:
```bash
python robust.py data/human_annotated_PPIs_brain.txt data/ms_seeds.txt ms.graphml 0.25 0.9 30 0.1
```
The positional arguments are:
```
[1] file providing the network in the form of an edgelist 
    (tab-separated table, columns 1 & 2 will be used)
[2] file with the seed genes (if table contains more than 
    one column they must be tab-separated; the first column 
    will be used only)
[3] path to output file
[4] initial fraction (alpha)
[5] reduction factor (beta)
[6] number of steiner trees to be computed
[7] threshold (theta)
```

The suffix of the path to the output file you specify, determine the format of the output.
You can either choose
- .graphml: A .graphml file is written that contains the following vertex properties: isSeed, significance, nrOfOccurrences, connected_components_id, trees
- .csv: A .csv file which contains a vertex table with #occurrences, %occurrences, terminal (isSeed) 
- everything else: An edge list

# Evaluating ROBUST

For a large-scale empirical evaluation of ROBUST, please follow the instructions given here: https://github.com/bionetslab/robust-eval.

# Citing ROBUST

Please cite ROBUST as follows:
- J. Bernett, D. Krupke, S. Sadegh1, J. Baumbach, S. P. Fekete, T. Kacprowski, M. List1, D. B. Blumenthal: Robust disease module mining via enumeration of diverse prize-collecting Steiner trees, *Bioinformatics* 38(6), pp. 1600-1606, https://doi.org/10.1093/bioinformatics/btab876.
