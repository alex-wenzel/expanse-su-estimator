#!/bin/bash
#SBATCH --job-name="hellompi"
#SBATCH --output="hellompi.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --mem=248G
#SBATCH --account=<<project*>>
#SBATCH --export=ALL
#SBATCH -t 01:30:00