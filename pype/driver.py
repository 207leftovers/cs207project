#!/usr/bin/env python3
#import pype
import sys
from pype.pipeline import *

for fname in sys.argv[1:]:
    Pipeline(source=fname)
