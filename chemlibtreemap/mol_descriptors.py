from rdkit.Chem import (
    MolFromSmiles, 
    Descriptors, 
    Descriptors3D, 
    AddHs, 
    AllChem
)
from typing import Callable, List


DESCRIPTORS_GENERATOR_REGISTRY = {}

def register_desc_generator(desc_name: str) -> Callable:
    """
    Register the descriptor generator in global dict to access by name
    Args:
        desc_name: descriptor name to be registered
    Returns:
        a decorator which adds descriptor generator to the registry
    """
    def decorator(desc_gen: Callable) -> Callable:
        DESCRIPTORS_GENERATOR_REGISTRY[desc_name] = desc_gen
        return desc_gen
    return decorator

def get_desc_generator(desc_name: str) -> Callable:
    """
    Get a descriptor generator by name
    Args:
        desc_name: descriptor name registered
    Returns:
        A descriptor generator working on single smiles
    """
    if desc_name not in DESCRIPTORS_GENERATOR_REGISTRY:
        raise ValueError(f"Descriptor {desc_name} not found")
    return DESCRIPTORS_GENERATOR_REGISTRY[desc_name]

def get_available_desc_generators() -> List[str]:
    """Returns a list of available descriptor generator names"""
    return list(DESCRIPTORS_GENERATOR_REGISTRY.keys())


@register_desc_generator("MolWeight")
def mol_weight_generator(smiles: str):
    return Descriptors.MolWt(MolFromSmiles(smiles))

@register_desc_generator("RingCount")
def ring_count_generator(smiles: str):
    return Descriptors.RingCount(MolFromSmiles(smiles))

@register_desc_generator("Fsp3")
def sp3_ratio_generator(smiles: str):
    return Descriptors.FractionCSP3(MolFromSmiles(smiles))

@register_desc_generator("GyrationRad")
def radius_of_gyration_generator(smiles: str):
    mol = MolFromSmiles(smiles)
    molh = AddHs(mol)
    AllChem.EmbedMolecule(molh)
    return Descriptors3D.RadiusOfGyration(molh)

# Additional descriptors can be registered with reference to:
# https://www.rdkit.org/docs/GettingStartedInPython.html#list-of-available-descriptors
