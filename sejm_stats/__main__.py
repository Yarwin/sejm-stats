#!/usr/bin/env python3

# Execute with
# $ python3 -m sejm_stats

import sys

if __package__ is None and not getattr(sys, 'frozen', False):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


import sejm_stats

if __name__ == '__main__':
    sejm_stats.main()
