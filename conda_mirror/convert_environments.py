"""Convert the channel on a set of environments to the local channel"""

import click
import yaml
import sys
import os.path as path
import os
import shutil


def _convert_environment(env_file: str, target_file: str, channel_url: str):
    arch_path, _ = path.split(target_file)
    os.makedirs(arch_path, exist_ok=True)
    with open(env_file, "rt") as f:
        env = yaml.safe_load(f)
    env["channels"].insert(0, channel_url)
    with open(target_file, "wt") as f:
        yaml.dump(env, f)


def _convert_environments(environment_path, target_path, channel_url):
    """
    Convert conda environment files found environment path to use channel URL as the channel
    """
    os.makedirs(target_path, exist_ok=True)
    env_list = path.join(environment_path, "environments.txt")
    with open(env_list, "tr") as f:
        envs = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    for env in envs:
        env_file = path.join(environment_path, env + ".yaml")
        target_file = path.join(target_path, env + ".yaml")
        _convert_environment(env_file, target_file, channel_url)

    new_env_list = path.join(target_path, "environments.txt")
    shutil.copyfile(env_list, new_env_list)

@click.command()
@click.argument("environment_path")
@click.argument("target_path")
@click.argument("channel_url")
def convert_environments(environment_path, target_path, channel_url):
    _convert_environments(environment_path, target_path, channel_url)
