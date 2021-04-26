#!/usr/bin/env python3

"""
Task definitions for doit.
Run the steps to generate and query our datasets using RDFox.
"""

from pathlib import Path
from os import path
from doit.tools import LongRunning

rdfox_path = "RDFox"  # change this if RDFox is not in your path
dir_path = path.dirname(path.realpath(__file__))
print(f"Running {rdfox_path} from {dir_path}")

data_csv = [
    'datasources/comtrade/ct-2018-exports.csv',
    'datasources/comtrade/ct-2018-imports.csv',
    'datasources/comtrade/HSCodeandDescription_2017.csv',
    'datasources/object_mappings/object_mappings.csv',
    'datasources/prodcom/PRC_2017_2016.csv',
    'datasources/prodcom/PRD_2016_20200617_185122.csv',
    'datasources/prodcom/PRD_2017_20200617_185035.csv',
    'datasources/prodcom/PRODCOM2014DATA_extract.csv',
    'datasources/prodcom/PRODCOM2016DATA.csv',
    'datasources/prodcom/PRODCOM2017DATA.csv',
    'datasources/prodcom/PRODCOM2018DATA.csv',
    'datasources/bgs/aggregates.csv',
]

data_scripts = [
    'datasources/comtrade/load_data.rdfox',
    'datasources/comtrade/map.dlog',
    'datasources/prodcom/load_data.rdfox',
    'datasources/prodcom/map.dlog',
    'datasources/object_mappings/load_data.rdfox',
    'datasources/object_mappings/map.dlog',
    'datasources/bgs/load_data.rdfox',
    'datasources/bgs/map.dlog',
]

ontology_ffs = [
    'probs.fss'
]

probs_data = [
    'data/probs_data.nt.gz'
]

reasoning_input = ontology_ffs + probs_data + [
    'scripts/reasoning/init.rdfox',
    'scripts/reasoning/load_data.rdfox',
    'scripts/reasoning/rules.dlog'
]


def task_preprocess():
    """Converts 'raw' data into CSV files for RDFox."""
    return {
        'file_dep': [
            'scripts/preprocess.py',
            'raw_data/ct-2018-exports.csv',
            'raw_data/ct-2018-imports.csv',
            'raw_data/HSCodeandDescription_2017.csv',
            'raw_data/PRD_2016_20200617_185122.csv',
            'raw_data/PRD_2017_20200617_185035.csv',
            'raw_data/PRODCOM2014DATA_extract.csv',
            'raw_data/PRODCOM2016DATA.csv',
            'raw_data/PRODCOM2017DATA.csv',
            'raw_data/PRODCOM2018DATA.csv'
        ],
        'targets': data_csv,
        'actions': [
            'python3 scripts/preprocess.py raw_data datasources'
        ],
    }


def task_conversion():
    """Reads CSV files, runs all the rules, and converts all of them into RDF."""
    return {
        'file_dep': data_csv + data_scripts + [
            "docs/_build/probs_rdf/output.ttl"
        ],
        'targets': probs_data,
        'actions': [
            "python scripts/conversion.py datasources/ data/probs_data.nt.gz"
        ],
        'verbosity': 2,
    }


def task_ontology_files():
    """Extract a temporary copy of the ontology file."""
    def extract_probs_fss():
        import importlib_resources
        with open("probs.fss", "wt") as f:
            f.write(importlib_resources.files("probs_ontology").joinpath("probs.fss").read_text())

    return {
        "targets": ["probs.fss"],
        "actions": [extract_probs_fss],
    }

def task_test_queries():
    """Reads the RDF file with the data, answers some queries."""
    return {
        'file_dep': probs_data + reasoning_input + [
            'scripts/reasoning/test_queries.rdfox',
            'scripts/reasoning/queries/query18.rq',
            'scripts/reasoning/queries/query18g.rq',
            'scripts/reasoning/queries/query26.rq',
            'scripts/reasoning/queries/query32.rq',
            'scripts/reasoning/queries/query33.rq',
            'scripts/reasoning/queries/queryWDF.rq',
            'scripts/reasoning/queries/queryHMC.rq',
            'scripts/reasoning/queries/queryHMO.rq',
            'scripts/reasoning/queries/queryHMObs.rq',
            'scripts/reasoning/queries/queryROC.rq',
        ],
        'targets': [
            'output/query18.csv',
            'output/query18g.csv',
            'output/query26.csv',
            'output/query32.csv',
            'output/query33.csv',
            'output/queryWDF.csv',
            'output/queryHMC.csv',
            'output/queryHMO.csv',
            'output/queryHMObs.csv',
            'output/queryROC.csv',
        ],
        'actions': [
            [rdfox_path, "sandbox", dir_path, "exec scripts/reasoning/test_queries"]
        ],
    }


def task_reasoning():
    """Reads the RDF file with the data and starts the RDFox endpoint."""
    cmd = [rdfox_path, "sandbox", dir_path, "exec scripts/reasoning/master"]
    return {
        'file_dep': reasoning_input + [
            'scripts/reasoning/master.rdfox'
        ],
        "uptodate": [False],
        'actions': [
            LongRunning(cmd, shell=False)
        ],
    }


def task_extract_rdf():
    return {
        "targets": ["docs/_build/probs_rdf/output.ttl"],
        "file_dep": (list(Path("docs").glob("*.md")) +
                     list(Path("docs/queries").glob("*.rq"))),
        "actions": [
            # Clean is needed for now at least, since Sphinx extension is not
            # properly responding to things being removed and caches them too
            # aggressively.
            #
            # Also when using jupyter-cache to avoid rerunning every notebook
            # every time, the cache needs to be cleared when the rdf output
            # changes (the --all option does this).
            "jupyter-book clean --all docs",
            ("jupyter-book build docs -v --builder=custom --custom-builder=probs_rdf "
             "--config docs/_config_extract_rdf.yml"),
        ],
    }
