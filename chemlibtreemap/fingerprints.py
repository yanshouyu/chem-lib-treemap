from typing import Callable, List
from mhfp.encoder import MHFPEncoder
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
import tmap
import numpy as np

FINGERPRINTS_GENERATOR_REGISTRY = {}

def register_fp_generator(fp_name: str) -> Callable:
    """
    Register the fp generator in global dict to access by name
    Args:
        fp_name: name used for accessing fingerprint generator
    Returns:
        A decorator which adds fp generator to the registry
    """
    def decorator(fp_generator: Callable) -> Callable:
        FINGERPRINTS_GENERATOR_REGISTRY[fp_name] = fp_generator
        return fp_generator
    return decorator

def get_fp_generator(fp_name: str) -> Callable:
    """
    Get a fingerprint generator by name
    Args:
        fp_name: name used for accessing fingerprint generator
    Returns:
        A fingerprint generator
    """
    if fp_name not in FINGERPRINTS_GENERATOR_REGISTRY:
        raise ValueError(f"Fingerprint {fp_name } not found")
    return FINGERPRINTS_GENERATOR_REGISTRY[fp_name]

def get_available_fp_generators() -> List[str]:
    """Returns a list of available fingerprint generator names"""
    return list(FINGERPRINTS_GENERATOR_REGISTRY.keys())


@register_fp_generator("MHFP6")
def mhfp6_fp_generator(smiles: str, d: int) -> tmap.VectorUint:
    mhfp_enc = MHFPEncoder(d)
    return tmap.VectorUint(mhfp_enc.encode(smiles))

@register_fp_generator("ECFP4")
def ecfp4_fp_generator(smiles: str, d: int) -> tmap.VectorUchar:
    mol = MolFromSmiles(smiles)
    fp = GetMorganFingerprintAsBitVect(mol, radius=2, nBits=d)
    return tmap.VectorUchar(list(fp))