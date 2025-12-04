import pytest

import os,sys

curr_dir=os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(curr_dir))
from app.main import gen_template


@pytest.mark.parametrize('win_file',
                         [os.path.join(curr_dir,'test_cases','mnte.win')]
                         )
def test_gen_param_file(win_file):
    assert not os.path.isfile(os.path.join(curr_dir,'params'))
    gen_template(win_file,curr_dir)
    assert os.path.isfile(os.path.join(curr_dir,'params'))
    os.remove(os.path.join(curr_dir,'params'))
