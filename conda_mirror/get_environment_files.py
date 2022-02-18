"""
Download an environment file list then download associated environments on that list
"""

import click
import requests
import os.path as path
import os


@click.command()
@click.argument("environment_list_url")
@click.argument("download_path")
def get_environment_files(environment_list_url: str, download_path: str):
    """
    Download ENVIRONMENT_LIST_URL, read in the environment file names, then download those to DOWNLOAD_PATH
    """

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