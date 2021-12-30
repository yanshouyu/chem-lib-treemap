import pytest
import chemlibtreemap

def test_descriptor_list():
    desc_list = chemlibtreemap.get_available_desc_generators()
    assert len(desc_list) > 0