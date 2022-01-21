import pytest
from conda_mirror.whitelist_environment import main
from contextlib import redirect_stdout
import io

def test_config_output():
    stdout_stream = io.StringIO()
    with redirect_stdout(stdout_stream):
        main(["test/igwn-py37.yaml", "test/igwn-py38.yaml"])
    stdout = stdout_stream.getvalue()
    with open("test/test_config.yaml", "rt") as f:
        check = f.read()
    assert check == stdout

