"""
A script with utilit functions for working within a slurm
environment to estimate job costs
"""

## A dictionary for converting values to gigabytes
## used by TRESWeights._parse_number_with_suffix_to_GB. Gives
## the multiplier necessary to convert a value in the scale 
## encoded by the prefix to gigabytes
SLURM_VALID_SUFFIXES = ["K", "M", "G", "T", "P"]

GB_CONV_D = {
    "K": 0.00000095367432,
    "M": 0.0009765625,
    "G": 1,
    "T": 1024,
    "P": 1048576
}

class SlurmSuffixError(Exception):
    pass

def parse_number_with_suffix_to_GB(number):
    """
    Returns a floating point number in megabytes. Following
    the slurm docs, the following suffixes are allowed:
    K, M, G, T, P 
    """
    ## Check if number doesn't have a suffix
    try:
        return float(number)
    except ValueError:
        ## Likely really does have a suffix,
        ## continue with function
        pass

    ## Make sure input is string
    number_str = str(number)

    ## Check if valid suffix, get multiplier
    suffix_str = number_str[-1]

    try:
        multiplier = GB_CONV_D[suffix_str]
    except KeyError:
        raise SlurmSuffixError(
            f"Suffix {suffix_str} not in {SLURM_VALID_SUFFIXES}"
        )

    return float(number_str[:-1]) * multiplier

