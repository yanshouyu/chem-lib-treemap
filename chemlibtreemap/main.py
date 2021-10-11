import argparse
from typing import Optional
import inspect
from . import draw_tmap
from .fingerprints import get_available_fp_generators
from .mol_descriptors import get_available_desc_generators

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=(
        "Create treemap based on fingerprints, with optional descriptors"
        " or features per compound as legend."
    ))
    parser.add_argument(
        "--matplotlib", action="store_true", 
        help="Draw treemap by matplotlib instead of default faerun")
    parser.add_argument(
        "--library", type=argparse.FileType("r"), 
        help=("library file with header in csv format, "
        "minimum columns: id, smiles. Other columns are treated as features"))
    parser.add_argument(
        "--output", 
        help="output destination folder where files will be generated under")
    parser.add_argument(
        "--fingerprint", choices=get_available_fp_generators(), default="MHFP6", 
        help="fingerprint type for creating treemap, default: MHFP6")
    parser.add_argument(
        "-d", "--dimension", type=int, default=1024, 
        help="fingerprint dimension, default: 1024")
    parser.add_argument(
        "--descriptors", default=[], 
        help=(
            f"Descriptors as node feature in treemap. Optional. "
            f"Choices: {get_available_desc_generators()}"
        ), 
        nargs="*")
    parser.add_argument(
        "--features", type=argparse.FileType("r"), required=False, 
        help=("additional NUMERICAL feature (float/int) table in csv format, "
        "header and id column required, "
        "id should be consistent with library table"))
    return parser


def single_treemap(args: Optional[argparse.Namespace] = None) -> None:
    if args is None:
        parser = create_parser()
        args = parser.parse_args()

    arg_dict = vars(args)
    arg_names = inspect.getfullargspec(draw_tmap.draw_tmap).args

    missing = set(arg_names) - set(arg_dict.keys())
    if missing:
        raise RuntimeError(f"Missing arguments: {missing}")
    tmap_args = {name: arg_dict[name] for name in arg_names}

    draw_tmap.draw_tmap(**tmap_args)

# TODO: additional arg parsing for matplotlib output, 
# fork entry point to draw_map.draw_tmap_mpl in single_treemap

# if __name__ == "__main__":
#     single_treemap()