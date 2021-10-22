import glob
import json

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from expanse_su_estimator.estimator import SUEstimator

#se = SUEstimator("test_examples/minimal_job.sh")
#se.estimate_cost()

for path in glob.glob("test_examples/*.sh"):
    se = SUEstimator(path)
    print(path)
    se.estimate_cost()
    print(se)
