"""
Cleans testing dirs after compression is executed
"""

import os


def clean(dr):
    files = os.listdir(dr)
    for f in files:
        path = os.path.join(dr, f)
        if os.path.isdir(path):
            clean(path)
        if ".zip" in f or 'log.txt' in f:
            os.remove(path)


dr = "../testing_dirs"
clean(dr)