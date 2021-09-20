# Example application of the PRObs ontology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5052757.svg)](https://doi.org/10.5281/zenodo.5052757)

This repository contains an example application of the PRObs ontology to querying data about a small subset of the UK production system.

## Prerequisites

- [RDFox](https://www.oxfordsemantic.tech) v4.1.0
- [Python](https://www.python.org) 3.8
- [Poetry](https://python-poetry.org)

In the following, we assume that both are installed and added to the PATH.

## Running

### Installation

The installation is simplified and automated using Poetry.
You only need to run:

```sh
poetry install
```

### Conversion

You need to convert the data only if you modified the mapping. Otherwise, go to the [Reasoning](#reasoning) section.

To convert the data, run `doit` from the root folder:

```sh
doit run conversion
```

This will add all the data sources and mappings to RDFox, apply rules, and save `data/probs_data.nt.gz`. It does this via the `probs-ontology` package; if this has been installed in editable mode (as specified in `pyproject.toml`, or with the `-e` option to `pip`) then any changes made within `probs-ontology` to the scripts will be picked up here, but you may need to force doit to rerun using the `doit run -as conversion` option.

This process takes place within the `_rdfox_working/conversion` folder, where a temporary set of scripts is assembled.

### Reasoning

To load the ontology and the data and start the RDFox endpoint, run:

```sh
doit run reasoning
```

Then go to [`http://localhost:12110/console/default`](http://localhost:12110/console/default) to run your SPARQL queries.

### Building the book/docs

Build using jupyter-book:

``` sh
jupyter-book build docs
```

The results are in `docs/_build`. This includes example queries.

## License

We include some data from other sources in the `raw_data` and `datasources` directories, but these are only for the purpose of illustrating the operation of the PRObs ontology and any use of this data is subject to the original source: [COMTRADE](https://comtrade.un.org/), [PRODCOM](https://ec.europa.eu/eurostat/web/prodcom) and [BGS](https://www.bgs.ac.uk/).

The other documents and code is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
