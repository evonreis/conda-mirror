#!/bin/bash
set -x
set -e

src_dir=$1
env_list_url=$2
channel=$3
repo_dir=$4
conda_dir=$5
channel_url=$6

# start python virtual environment
source $src_dir/.venv/bin/activate

# download environment files
get-environment-files $env_list_url $src_dir/environments

# have to convert environments to point at this repo
mkdir -p '$src_dir/environments'
convert-environments $src_dir/environments $repo_dir/environments $channel_url

# whitelist all the environments
whitelist-environment $src_dir/environments/linux-64/* > $src_dir/config.yaml

# mirror repo
conda-mirror --upstream-channel $channel --target-directory $repo_dir --platform linux-64 --config $src_dir/config.yaml \
  --no-progress --include-depends


$conda_dir/bin/conda index $repo_dir


