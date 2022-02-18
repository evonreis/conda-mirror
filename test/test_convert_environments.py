from conda_mirror.convert_environments import _convert_environments
import shutil
import yaml


def test_environment_conversion():
    shutil.rmtree("test/repo", ignore_errors=True)
    _convert_environments("test/environments", "test/repo", "http://test.com")
    with open("test/repo/linux-64/igwn-py37.yaml","rt") as f:
        env = yaml.safe_load(f)

    assert len(env["channels"]) == 2
    assert env["channels"][0] == "http://test.com"
    assert env["channels"][1] == "conda-forge"

    with open("test/repo/linux-64/igwn-py38.yaml","rt") as f:
        env = yaml.safe_load(f)

    assert len(env["channels"]) == 2
    assert env["channels"][0] == "http://test.com"
    assert env["channels"][1] == "conda-forge"