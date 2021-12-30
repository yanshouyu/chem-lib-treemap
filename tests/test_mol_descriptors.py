import pytest
from chemlibtreemap import mol_descriptors

def test_descriptor_list():
    desc_list = mol_descriptors.get_available_desc_generators()
    assert len(desc_list) > 0