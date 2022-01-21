"""
Take as input an conda environment yaml file.  Output a conda-mirror configuration that blacklists every package except
those given in the environment file.
"""

import yaml