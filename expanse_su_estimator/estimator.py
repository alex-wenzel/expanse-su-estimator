import glob
import json
import sys
from .sbatch_parser import SBATCHScript

QUEUE_MAX_WALLTIME_HOURS = {
    "compute": 48,
    "shared": 48,
    "large-shared": 48,
}

QUEUE_MEM_GIGS_PER_NODE = {
    "compute": 256,
    "shared": 256,
    "large-shared": 2000
}

def estimate_sus(path):
    script = SBATCHScript(path)
    script.parse()

    sus = 0

    ## Check if shared or exclusive
    try:
        partition = script["partition"]
    except KeyError: ## This is hacky. Parser needs to have conversion from shorthand.
        partition = script["p"] 

    if partition == "compute":
        sus = 128 * int(script["nodes"])

    else:
        mem = int(script["mem"].strip("G"))
        mem_frac = mem / (QUEUE_MEM_GIGS_PER_NODE[partition])
        sus = max(mem_frac, int(script["ntasks-per-node"]) * int(script["nodes"]))

    ## Include walltime
    try:
        wt_tokens = script["t"].split(":")
        hours, minutes, seconds = list(map(int, wt_tokens))

        if (minutes > 0) or (seconds > 0):
            hours += 1

        sus *= hours
    except KeyError:
        print("WARNING: No walltime specified. Maximum for queue will be assumed")
        print("For more accurate results, specify a walltime in with the following format: ")
        print("\t#SBATCH -t <HH>:<MM>:<SS>")

        sus *= QUEUE_MAX_WALLTIME_HOURS[partition]


    return sus

if __name__ == "__main__":
    answer_key = json.load(open("test_examples/test_examples_real_su.json", 'r'))
    
    for script_path in glob.glob("test_examples/expanse*.sh"):
        script_name = script_path.split('/')[-1].split('.')[0]

        print(script_path, answer_key[script_name], estimate_sus())