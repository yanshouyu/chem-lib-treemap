import pytest
from chemlibtreemap import fingerprints

def test_fp_list():
    fp_list = fingerprints.get_available_fp_generators()
    assert len(fp_list) > 0

