"""
Download an environment file list then download associated environments on that list
"""

import click
import requests
import os.path as path
import os
import shutil
from pathlib import Path

# Directories that should never be deleted, even though they're deeper than top level
PROTECTED = {
    Path("/usr/local"),
    Path("/var/lib"),
    Path("/var/log"),
    Path("/home"),
}

def check_safe_to_delete(path, min_depth=3):
    p = Path(path).expanduser().resolve(strict=True)

    if not p.is_dir():
        raise ValueError(f"Not a directory: {p}")

    # p.parts for "/" is ("/",), for "/etc" is ("/", "etc"), for "/home/me/x" is ("/", "home", "me", "x")
    if len(p.parts) < min_depth:
        raise ValueError(f"Refusing: {p} is too shallow (root or top-level)")

    if p in PROTECTED:
        raise ValueError(f"Refusing: {p} is protected")

    if p == Path.home().resolve():
        raise ValueError("Refusing: that's your home directory")

    # A mount point is usually something you don't want to rmtree
    if p.is_mount():
        raise ValueError(f"Refusing: {p} is a mount point")

    return p

@click.command()
@click.argument("environment_list_url")
@click.argument("download_path")
def get_environment_files(environment_list_url: str, download_path: str):
    """
    Download ENVIRONMENT_LIST_URL, read in the environment file names, then download those to DOWNLOAD_PATH
    """

    # delete environment download path then recreate it
    check_safe_to_delete(Path(download_path))
    shutil.rmtree(download_path, ignore_errors=True);
    os.makedirs(download_path)

    result = requests.get(environment_list_url)
    if result.status_code != 200:
        raise click.ClickException(f"Could not download environment list at {environment_list_url}: status code {result.status_code}")

    env_file = path.join(download_path, "environments.txt")
    with open(env_file, "wt") as f:
        f.write(result.text)

    # get base url
    base_url, _ = path.split(environment_list_url)

    names = result.text.strip().split()
    for name in names:
        file = name + ".yaml"
        url = path.join(base_url, file)
        result = requests.get(url)
        if result.status_code != 200:
            raise click.ClickException(f"Could not download environment at {url}: status code {result.status_code}")

        out_name = path.join(download_path, file)

        base_path, _ = path.split(out_name)
        os.makedirs(base_path, exist_ok=True)
        with open(out_name, "wt") as f:
            f.write(result.text)
