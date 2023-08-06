import os
import sys
from subprocess import check_call

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
check_call(
    (
        "py.test -v --log-level=debug --cov=shtab"
        " --cov-report=xml --cov-report=term-missing --durations=0"
        + (" ".join([""] + sys.argv[1:]))
    ),
    shell=True,
    env=dict(os.environ, PYTHONPATH=REPO_ROOT),
)
