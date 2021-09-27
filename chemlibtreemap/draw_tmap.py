import os
import tmap
from faerun import Faerun
import pandas as pd
import numpy as np
from typing import Optional, List, TextIO
from .fingerprints import get_fp_generator
from .mol_descriptors import get_desc_generator
from chemlibtreemap import fingerprints

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
    if len(feature_df.columns) == 0:
        feature_df["random_value"] = np.random.rand(len(feature_df))
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
            lambda dt: True if dt=="object" else False
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
    libdf = pd.read_csv(library, index_col='id')

    if descriptors:
        for desc_name in descriptors:
            desc_func = get_desc_generator(desc_name)
            libdf[desc_name] = libdf['smiles'].apply(desc_func)
    
    if features:
        feature_df = pd.read_csv(features, index_col='id')
        libdf = libdf.join(feature_df)
    
    libdf.to_csv(os.path.join(output, "data.csv"))
    
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

    if matplotlib:
        draw_mpl(x, y, s, t, libdf, output)
    else:
        draw_faerun(x, y, s, t, libdf, output)
