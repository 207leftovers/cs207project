#!/usr/bin/env python3
import pype
import sys

for fname in sys.argv[1:]:
  pype.Pipeline(source=fname)
