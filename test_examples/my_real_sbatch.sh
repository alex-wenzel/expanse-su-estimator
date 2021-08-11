#!/bin/bash
#SBATCH --job-name="my_script"
#SBATCH --output="my_script.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --export=ALL
#SBATCH --account=ddp242
#SBATCH --mail-user=myemail@examplesbatch.com
#SBATCH -t 48:00:00
#!/bin/bash

module load singularitypro

        