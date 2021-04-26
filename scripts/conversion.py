#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import shutil

from probs_ontology import load_datasource, Datasource
from probs_ontology.runner.probs_runner import probs_convert_data

import logging

if os.environ.get("PROBS_DEBUG"):
    log_level = logging.DEBUG
else:
    log_level = logging.INFO
logging.basicConfig(level=log_level)


HERE = Path(__file__).parent


if __name__ == "__main__":
    working_dir = HERE / "_rdfox_working/conversion"
    if working_dir.exists():
        if working_dir.joinpath("__master.rdfox").exists():
            logging.warning("Clearing working dir %r", working_dir)
            shutil.rmtree(working_dir)
        elif list(working_dir.glob("*")):
            logging.error("Working dir contains unexpected files! Not clearing it, but this may cause errors.")

    datasources = Path(sys.argv[1])
    sources = [
        load_datasource(p)
        for p in datasources.iterdir()
        if p.is_dir()
    ]

    # Additional datasource for the system definitions
    sources.append(
        Datasource(
            input_files={"data/system.ttl": HERE / "../docs/_build/probs_rdf/output.ttl"},
            load_data_script="import system.ttl\n"
        )
    )

    output_filename = Path(sys.argv[2])
    output_filename.parent.mkdir(parents=True, exist_ok=True)
    probs_convert_data(sources, output_filename, working_dir=working_dir)
