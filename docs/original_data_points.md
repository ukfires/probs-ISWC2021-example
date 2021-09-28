---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Retrieve original data points

First, let's check we can retrieve the original data points consistently.

## Behind-the-scenes

We start by loading SPARQL queries, and sends them to RDFox to be answered against the pre-converted data. For simplicity the details are hidden in [a separate Python file](example_data.py):

```{code-cell} ipython3
from example_data import results
```

## Prodcom

We can retrieve original data points from Prodcom linked to a classification code (`08121230`) using the following SPARQL query:

```{literalinclude} queries/original_prodcom.rq
:language: sparql
```

```{code-cell} ipython3
results["original_prodcom"]
```

The results are exactly the ones we expect (Figure 3 of the paper):

```{figure} figures/original_prodcom.svg
:name: Original Prodcom
:width: 100%

All the initial data points from Prodcom.
```

## BGS Minerals Yearbook

If we want to retrieve the data points specific of the BGS Minerals Yearbook dataset mentioned in [[Add reference to data sources page]]:

```{figure} figures/original_bgs.svg
:name: Original Prodcom
:width: 100%

All the initial data points from BGS.
```

We can use the following query:

```{literalinclude} queries/original_bgs.rq
:language: sparql
```

```{code-cell} ipython3
results["original_bgs"]
```
