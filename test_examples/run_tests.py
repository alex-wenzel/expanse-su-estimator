import glob
import json

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from expanse_su_estimator.estimator import estimate_sus

answer_key = json.load(open("test_examples_real_su.json", 'r'))
    
for script_path in glob.glob("expanse*.sh"):
    print(script_path)
    script_name = script_path.split('/')[-1].split('.')[0]

    print(script_path, answer_key[script_name], estimate_sus(script_path))

    print('\n')