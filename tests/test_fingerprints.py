import pytest
import chemlibtreemap

def test_fp_list():
    fp_list = chemlibtreemap.get_available_fp_generators()
    assert len(fp_list) > 0

