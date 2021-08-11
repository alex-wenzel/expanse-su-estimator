#!/bin/bash
#SBATCH --job-name="hellohybrid"
#SBATCH --output="hellohybrid.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH --mem=248G
#SBATCH --account=<<project*>>
#SBATCH --export=ALL
#SBATCH -t 01:30:00