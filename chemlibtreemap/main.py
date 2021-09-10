import argparse
from typing import Optional
import inspect
from . import draw_tmap

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matplotlib", action="store_true", 
        help="Draw treemap by matplotlib instead of default faerun")
    parser.add_argument(
        "--library", type=argparse.FileType("r"), 
        help="library file with header in csv format, one column should be smiles")
    parser.add_argument(
        "--output", help=(
            "output destination, if using faerun (default), "
            "file extension is not needed"))
    parser.add_argument(
        "--fingerprint", choices=["MHFP6", "ECFP4"], default="MHFP6", 
        help="fingerprint type for creating treemap")
    parser.add_argument(
        "-d", "--dimension", type=int, default=1024, 
        help="dfingerprint dimension")
    parser.add_argument(
        "--descriptors", default=[], 
        help=(
            f"Descriptors as node feature in treemap. Optional."
            # TODO: enumerate choices
            # f"choices: {list(mol_descriptors.REGISTERED.keys())}"
        ), 
        nargs="*")
    parser.add_argument(
        "--features", type=argparse.FileType("r"), required=False, 
        help="additional feature table with header in csv format")
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