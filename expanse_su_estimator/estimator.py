"""
This script defines a class to retrieve system billing weights and estimate
the cost of an SBATCH job script
"""

import glob
import json
import sys

from .sbatch_parser import SBATCHScript
from .tres_parser import TRESWeights
from .utils import parse_number_with_suffix_to_GB, SlurmSuffixError

## Valid sbatch param names for important fields
SBATCH_COST_PARAMS_L = ["partition", "cpu", "mem", "node"]

## Note - SBATCHScript removes dashes
SBATCH_COST_PARAMS_D = {
    "partition": ["p", "partition"],
    "cpu": ["ntasks-per-node"],
    "mem": ["mem"],
    "node": ["N", "nodes"]
}

class SUEstimator:
    def __init__(self, sbatch_path):
        """
        Initializes tres weights and parses job script
        """
        self.tres_weights = TRESWeights()
        self.tres_weights.parse()

        self.sbatch_path = sbatch_path
        self.sbatch_script = SBATCHScript(sbatch_path)
        self.sbatch_script.parse()

        self.maximum_param = None
        self.maximum_param_val = None
        self.cost = None

    def estimate_cost(self):
        """
        Function for scoring based on tres weights
        """
        user_vals_d = {}
        for param_name_str in SBATCH_COST_PARAMS_L:
            param_keys_l = SBATCH_COST_PARAMS_D[param_name_str]
            try:
                user_vals_d[param_name_str] = parse_number_with_suffix_to_GB(
                    self.sbatch_script[param_keys_l]
                )
            except SlurmSuffixError:
                user_vals_d[param_name_str] = self.sbatch_script[param_keys_l]
        
        ## Update cores to total cores requested
        user_vals_d["cpu"] = user_vals_d["cpu"] * user_vals_d["node"]

        ## Convert memory to total memory requested and convert to gigs
        user_vals_d["mem"] = user_vals_d["mem"] * user_vals_d["node"]
        #user_vals_d["mem"] = user_vals_d["mem"] / 1024.0

        ## Get weighted resource values
        weighted_tres_d = {
            tres_name: self.tres_weights.get_partition_value(
                user_vals_d["partition"],
                tres_name
            ) * user_vals_d[tres_name]
            for tres_name in ["cpu", "mem", "node"]
        }

        ## Get which parameter is driving cost
        self.maximum_param = max(weighted_tres_d, key = weighted_tres_d.get)

        self.maximum_param_val = weighted_tres_d[self.maximum_param]

        ## Parse walltime
        time_tokens_l = self.sbatch_script[["t", "time"]].split(":")
        hours, minutes, seconds = list(map(int, time_tokens_l))
        if (minutes > 0) or (seconds > 0):
            hours += 1

        ## Get final cost
        self.cost = (self.maximum_param_val / 3600) * hours

    def __str__(self):
        if self.cost is None:
            return "You must call estimate_score() before calling report()"

        r = "=========\n"
        ## Introduction
        r += "Expanse computes SU cost using a combination of "
        r += "cores, memory, and nodes used, depending on the parition "
        r += "(queue).\n\n"

        ## Add which queue the user choose
        part_name = self.sbatch_script[SBATCH_COST_PARAMS_D["partition"]]
        r += f"The partition for this job is "
        r += "\033[1m"+part_name+"\033[0m\n\n"

        ## Add what the weights for the queue are
        r += "This partition has the following weightings (per hour):\n"
        
        r += "\tCores: \033[1m"
        core_weight = str(
            self.tres_weights.get_partition_value(part_name, "cpu")/3600
        )
        r += core_weight
        r += " per CPU\033[0m\n"

        r += "\tMemory: \033[1m"
        memory_weight = str(
            self.tres_weights.get_partition_value(part_name, "mem")/3600
        )
        r += memory_weight
        r += " per GB\033[0m\n"

        r += "\tNodes: \033[1m"
        node_weight = str(
            self.tres_weights.get_partition_value(part_name, "node")/3600
        )
        r += node_weight
        r += " per node\033[0m\n\n"

        ## Print out the result values and say which one was chosen
        r += "This job requests the following resources: \n"
        
        r += "\tCores: \033[1m"
        user_cores = str(
            self.sbatch_script[SBATCH_COST_PARAMS_D["cpu"]]
        )
        r += user_cores
        r += "\033[0m\n"

        r += "\tMemory: \033[1m"
        user_mem = str(
            parse_number_with_suffix_to_GB(
                self.sbatch_script[SBATCH_COST_PARAMS_D["mem"]]
            )
        )
        r += user_mem
        r += " GB\033[0m\n"

        r += "\tNodes: \033[1m"
        user_nodes = str(
            self.sbatch_script[SBATCH_COST_PARAMS_D["node"]]
        )
        r += user_nodes
        r += "\033[0m\n\n"
    
        ## Print out the final computation
        r += "The cost comes from the maximum of the following computations:\n"
        
        r += f"\t{user_cores} cores * {core_weight} "
        r += f"= {float(user_cores) * float(core_weight)}\n"

        r += f"\t{user_mem} GB * {memory_weight} "
        r += f"= {float(user_mem) * float(memory_weight)}\n"

        r += f"\t{user_nodes} nodes * {node_weight} "
        r += f"= {float(user_nodes) * float(node_weight)}\n\n"

        r += "The obtain an \033[1mUPPER BOUND\033[0m cost estimate, "
        r += "the maximum value is multiplied by the number of hours, "
        r += "rounded up to the nearest hour.\n\n"

        time_tokens_l = self.sbatch_script[["t", "time"]].split(":")
        hours, minutes, seconds = list(map(int, time_tokens_l))
        if (minutes > 0) or (seconds > 0):
            hours += 1
        
        r += f"This job requests {hours} hours (rounded up), so the maximum "
        r += "estimated cost of this job is \033[1m "
        r += f"{self.maximum_param_val/3600} * {hours} = {self.cost} "
        r += "service units.\033[0m\n"

        return r + "========="
