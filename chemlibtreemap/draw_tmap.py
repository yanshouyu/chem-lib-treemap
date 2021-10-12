import os
import pickle
import tmap
from faerun import Faerun
import pandas as pd
import numpy as np
from typing import Optional, List, TextIO
import logging
from .fingerprints import get_fp_generator
from .mol_descriptors import get_desc_generator
from chemlibtreemap import fingerprints

def create_logger(save_dir):
    "create a simple logger with both streaming handler and file handler"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    fh = logging.FileHandler(os.path.join(save_dir, "tmap.log"), mode="w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


def draw_mpl(
    x: tmap.VectorFloat, 
    y: tmap.VectorFloat, 
    s: tmap.VectorUint, 
    t: tmap.VectorUint, 
    libdf: pd.DataFrame, 
    output: str
):
    pass

def draw_faerun(
    x: tmap.VectorFloat, 
    y: tmap.VectorFloat, 
    s: tmap.VectorUint, 
    t: tmap.VectorUint, 
    libdf: pd.DataFrame, 
    output: str
) -> None:
    feature_df = libdf[[col for col in libdf.columns if col not in ["smiles"]]]
    feature_dct = feature_df.to_dict('list')
    scatter_data = {
        "x": x, 
        "y": y, 
        "c": list(feature_dct.values()), 
        "labels": libdf["smiles"].tolist()
    }
    fr = Faerun(view="front", coords=False)
    fr.add_scatter(
        "tmap", 
        scatter_data, 
        point_scale=5, 
        categorical=feature_df.dtypes.apply(
            lambda dt: True if dt in ("object", "int") else False
        ).tolist(), 
        colormap=feature_df.dtypes.apply(
            lambda dt: "Set1" if dt in ("object", "int") else "rainbow"
        ).tolist(), 
        has_legend=True,
        legend_title=[f"feature_{k}" for k in feature_dct.keys()], 
        series_title=list(feature_dct.keys()), 
        shader="smoothCircle"
    )
    fr.add_tree("tmap_tree", {"from": s, "to": t}, point_helper="tmap")
    fr.plot("tmap", path=output, template="smiles")



def draw_tmap(
    library: TextIO, 
    output: str, 
    fingerprint: str, 
    dimension: int, 
    descriptors: List[str], 
    features: Optional[TextIO], 
    matplotlib: bool, 
) -> None:
    # check output dir existance
    if (not os.path.exists(output)) or (not os.path.isdir(output)):
        os.makedirs(output)
    logger = create_logger(save_dir=output)
    logger.info(f"library file: {library.name}")
    logger.info(f"output folder path: {output}")
    logger.info(f"fingerprint: {fingerprint}")
    logger.info(f"fingerprint dimension: {dimension}")
    logger.info(f"chemical descriptors: {descriptors}")
    logger.info(f"additional feature file: {features.name if features else None}")

    libdf = pd.read_csv(library, index_col='id')
    logger.debug(f"loaded {len(libdf)} compounds")

    if descriptors:
        for desc_name in descriptors:
            desc_func = get_desc_generator(desc_name)
            libdf[desc_name] = libdf['smiles'].apply(desc_func)
            logger.debug(f"additional descriptor {desc_name} added")

    if features:
        feature_df = pd.read_csv(features, index_col='id')
        isnum_cols = [
            str(dt).startswith('float') or str(dt).startswith('int') 
            for dt in feature_df.dtypes
        ]
        if not all(isnum_cols):
            logger.warning("not all additional features are numeric, "
            "ignoring non-numeric feature columns")
            feature_df = feature_df.loc[:, isnum_cols]
        libdf = libdf.join(feature_df)
        logger.debug(f"additional features: {feature_df.columns.tolist()} added")
    
    # add random number column as placeholder feature if needed
    if len(set(libdf.columns) - set(["smiles"])) == 0:
        logger.warning(
            "no feature columns for compound library, "
            "adding random numbers as placeholder"
        )
        libdf["random_value"] = np.random.rand(len(libdf))
    libdf.to_csv(os.path.join(output, "data.csv"))
    logger.debug(f"saved library table to {os.path.join(output, 'data.csv')}")
    
    fp_gen = get_fp_generator(fingerprint)
    fp_list = libdf['smiles'].apply(fp_gen, d=dimension).tolist()

    lf = tmap.LSHForest(dimension)
    if fingerprint == "MHFP6":
        lf.batch_add(fp_list)
    else:
        enc = tmap.Minhash(dimension)
        lf.batch_add(enc.batch_from_binary_array(fp_list))
    lf.index()

    x, y, s, t, _ = tmap.layout_from_lsh_forest(lf)
    logger.debug("tmap layout calculated")
    # tmap.VectorFloat not dumpable, convert them to list
    with open(os.path.join(output, "layout.pkl"), "wb") as f:
        pickle.dump({
            "x": list(x), 
            "y": list(y), 
            "s": list(s), 
            "t": list(t), 
        }, f)
        logger.debug("layout data (x, y, s, t) saved.")

    if matplotlib:
        draw_mpl(x, y, s, t, libdf, output)
    else:
        draw_faerun(x, y, s, t, libdf, output)
    logger.debug("tmap drawn. All clear.")
