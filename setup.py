import os
from setuptools import setup, find_packages

with open("README.md", "r") as rf:
    README = rf.read()

with open("LICENSE", "r") as lf:
    LICENSE = lf.read()

# TODO: get version from chemlibtreemap.__init__.py
def get_version():
    return "0.0.1"

setup(
    name="chemlib_treemap", 
    packages=find_packages(), 
    version=get_version(), 
    description="Draw TMAP for chemical libraries", 
    author="Shouyu Yan", 
    author_email="yan.shouyu@foxmail.com", 
    url="https://github.com/yanshouyu/chem-lib-treemap", 
    # TODO: project_urls dict, keys: Documentation, Source, ...
    license=LICENSE, 
    install_requires=[
        "faerun", 
        "matplotlib", 
        "pandas", 
        "tmap", 
        "mhfp", 
    ], 
    entry_points={
        "console_scripts": [
            "single-treemap = chemlibtreemap.main:single_treemap", 
        ]
    }, 
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Chem-Informatics'
    ],
    keywords=["Cheminformatics", "TreeMap", "Visualization"], 
)