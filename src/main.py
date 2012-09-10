# setting up path first!
import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SRC_DIR, "lib")
if not LIB_DIR in sys.path:
    sys.path.append(LIB_DIR)

import dcf
app = dcf.app
