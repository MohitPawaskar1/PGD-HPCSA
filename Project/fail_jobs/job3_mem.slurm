#!/bin/bash
#SBATCH --mem=10M
python3 - << 'EOPY'
a = 'x' * (1024*1024*200)
print(len(a))
EOPY
