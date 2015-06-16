#!/usr/bin/env python

import os
import sys

import nose

# Let settings know we're running as a unittest.
os.environ['pinterest_unittest'] = 'True'

__test__ = False  # Not a test to be collected by Nose itself.

if __name__ == '__main__':
    # Add ROOT and ROOT.libs to sys.path
    sys.path.insert(0, os.path.join(os.getcwd(), 'libs'))
    sys.path.insert(0, os.getcwd())

    argv = sys.argv + ['--logging-clear-handlers']
    nose.main(argv=argv, defaultTest='tests')