"""
This file defines a class that parses and represents an SBATCH submission
script
"""

class SBATCHScript:
    def __init__(self, path):
        self.path = path
        self.args = {}

    def __getitem__(self, key):
        return self.args[key]

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


if __name__ == "__main__":
    s = SBATCHScript("test_examples/expanse_shared_example.sh")
    s.parse()