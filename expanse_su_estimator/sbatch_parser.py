"""
This file defines a class that parses and represents an SBATCH submission
script
"""

class SBATCHScript:
    def __init__(self, path):
        self.path = path
        self.args = {}

    def __getitem__(self, key):
        if type(key) == list:
            return self.multiple_key_query(key)
        else:
            return self.args[key]

    def __str__(self):
        return '\n'.join([
            f"{key}: {value}"
            for key, value in self.args.items()
        ])

    def parse(self):
        for line in open(self.path, 'r').readlines():
            if not line.startswith("#SBATCH"):
                continue

            tokens = line.split()[1:]

            arg, val = None, None

            ## parse args with '--' and '='
            if len(tokens) == 1:
                arg, val = tokens[0].split('=')
                
            ## parse args with '-'
            else:
                arg, val = tokens

            arg = arg.strip("-")

            self.args[arg] = val

    def multiple_key_query(self, keys):
        """
        A function to allow for querying of parameters
        that can have multiple names, .e.g., -N, --nodes
        """
        for key in keys:
            try:
                return self.args[key]
            except KeyError:
                continue

        raise KeyError(f"None of {keys} in sbatch arguments") 

if __name__ == "__main__":
    s = SBATCHScript("test_examples/expanse_shared_example.sh")
    s.parse()
