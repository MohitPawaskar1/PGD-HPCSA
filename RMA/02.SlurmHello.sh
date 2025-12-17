#!/bin/bash
#SBATCH --nodelist=cdac@cdac-compute
#SBATCH --output=cdac@cdac-storage:/sorage/output/
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --time=00:05:00


touch Hello.py &> dev/null
echo "print ("Hello, from SLURM!")" >> Hello.py  &> dev/null
sleep 30 
