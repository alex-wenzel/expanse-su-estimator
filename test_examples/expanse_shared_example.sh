#!/bin/bash
#SBATCH -p shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=40G
#SBATCH -t 01:00:00
#SBATCH -J job.8
#SBATCH -A <<project*>>
#SBATCH -o job.8.%j.%N.out
#SBATCH -e job.8.%j.%N.err
#SBATCH --export=ALL
