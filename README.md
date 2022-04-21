# K-anonymity for EGoT

LeFevre, DeWitt, and Ramakrishnan proposed a multi-dimensional model for k-anonymization and a greedy algorithm for k-anonymization [1]. The Mondrian algorithm aims at approximating the optimal anonymization contrasted with finding it. Essentially, it finds a solution by partitioning the instances with respect to all quasi-identifiers in a Mondrian manner. That is, all partitions used are axis-aligned. The proposed approach has a far better complexity than previously proposed methods for achieving K-anonymity. The fact that it relies on a greedy algorithm gives us the benefit of achieving anonymization in $O(n log n)$ time complexity. 

## Install requirements
```
    pip3 install -r requirements.txt
```
## Run configuration script
The configuration script clones an implementation of the Mondrian algorithm before using it for EGoT topological IDs. 

To run the configuration script:
```bash
    source configure.sh
```

## Run ID Generator
The `generate_rand_data` script creates multiple random records based on EGoT topological grouping. 

> The script allows for generating complete random IDs __or__ based on IEEE 13 node test feeder. It outputs the data into a CSV file named `random_ids.csv`

To run generate random IDs:
```
    python3 generate_rand_data.py r <number>
```

To run generate IEEE 13 node feeder data:
```
    python3 generate_rand_data.py ieee
```

## Run Anonymizer
```bash
    python3 k_anonymizer.py -f input_file.csv
```
### Program Arguments
* __f__ argument: The input file name 
    * run: `python3 k_anonymizer.py -f input_file.csv`
    * default: `none`
* __K__ argument (optional): The `K` value for K-anonymity
    * run: `python3 k_anonymizer.py -K <value of K>`
    * default: `2`
* __H__ argument (optional): The `H` value for the generalization hierarchy
    * run: `python3 k_anonymizer.py -H <value of H>`
    * default: `dynamically picked based on the K value`
* __O__ argument: The output file name 
    * run: `python3 k_anonymizer.py -O ouput_file.csv`
    * default: `none`

----

## References
[1] K. LeFevre, D.J. DeWitt, and R. Ramakrishnan. Mondrian multidimensional k-
anonymity. In 22nd International Conference on Engineering, pages 25–25, 2006