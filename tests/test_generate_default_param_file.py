import pytest

import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.main import gen_template

@pytest.mark.parametrize('win_file',
                         ['test_cases/mnte.win']
                         )
def test_gen_param_file(win_file):
    assert()