"""
This script defines a function to find the TRESBillingWeights of a 
Slurm system running locally. This script assumes that it can call
`scontrol show partition` 
"""

import subprocess
import sys

from .utils import parse_number_with_suffix_to_GB


class TRESWeights:
    def __init__(self):
        self.weights = {}

    def __str__(self):
        return '\n'.join([
            f"{key}: {value}"
            for key, value in self.weights.items()
        ])

    def parse(self):
        try:
            cmd_str = subprocess.check_output(
                "scontrol show partition",
                shell = True
            ).decode("utf-8")
        except subprocess.CalledProcessError:
            raise RuntimeError(
                (
                    "`scontrol show partition` failed with non-zero exit code\n"
                    "Are you sure you're on a cluster running slurm?"
                )
            )

        for partition_str in cmd_str.strip('\n').split('\n\n'):
            partition_name_str = (
                partition_str.split('\n')[0]
                .split('=')[1]
            )

            if partition_name_str == "aws":
                continue

            self.weights[partition_name_str] = {}

            weights_str = partition_str.split('\n')[-1].strip()

            weight_toks_l = (
                weights_str.strip("TRESBillingWeights=")
                .split(',')
            )
            
            for weight_toks_str in weight_toks_l:
                tres, val = weight_toks_str.split('=')
                val_mb = parse_number_with_suffix_to_GB(val)
                self.weights[partition_name_str][tres] = val_mb

    def get_partition_value(self, partition_name, tres_name):
        return self.weights[partition_name][tres_name]


