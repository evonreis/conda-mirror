"""
Take as input an conda environment yaml file.  Output a conda-mirror configuration that blacklists every package except
those given in the environment file.
"""

import click
import yaml
import sys


def read_conda_environments(env_paths: list):
    """
    Read in a list of paths to yaml conda environment definitions.

    Used to create package whitelists for conda-mirror

    :param env_paths: A list of paths to conda environment definition yaml files
    :return: a list of packages defined in the environment.
    The package is a dictionary with a "name" member and optional
    "version" and "build" members.
    """
    packages = []
    for env_path in env_paths:
        with open(env_path, "rt") as f:
            env = yaml.safe_load(f)
            for dep in env["dependencies"]:

                # dep is in format <name>=<version>=<build>
                # but version and build are optional

                pkg_vals = dep.strip().split('=')
                pkg = {"name": pkg_vals[0]}
                if len(pkg_vals) > 1:
                    pkg["version"] = pkg_vals[1]
                if len(pkg_vals) > 2:
                    pkg["build"] = pkg_vals[2]
                packages.append(pkg)
    return packages


def print_whitelist_config(packages):
    """
    Print a configuration file for conda-mirror that whitelists every package in packages.

    :param packages: A list of package specifications such as returned by read_conda_environment()
    :returns: none
    """
    # output blacklist of all packages, then 'packages' as white list
    config = {"blacklist": [{"name": '*'}], "whitelist": packages}

    # create the whitelist
    yaml.dump(config, sys.stdout)


def main(conda_env_defs):
    packages = read_conda_environments(conda_env_defs)
    print_whitelist_config(packages)


@click.command()
@click.argument("conda_env_defs", nargs=-1)
def whitelist_environment(conda_env_defs: list):
    """
    Convert conda environment definition files into a conda_mirror white-list configuration.

    Multiple yaml files will be combined into a single whitelist.

    Output is to stdout.

    conda_env_defs: paths to conda environment definition yaml files
    """
    main(conda_env_defs)
