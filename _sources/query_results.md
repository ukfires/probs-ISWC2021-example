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

# Query results

Python code might be used to perform some operations.
For instance, the following snippet loads libraries and SPARQL queries, and sends them to RDFox to be answered against the pre-converted data:

```{code-cell} ipython3
from pathlib import Path
import pandas as pd
from probs_ontology.runner.probs_runner import probs_query_data

queries = {
    p.stem: p.read_text()
    for p in Path("queries").glob("*.rq")
}

results = probs_query_data("../data/probs_data.nt.gz", queries)
```

<!-- ```{code-cell} ipython3
obs_short_labels = {
    "https://ukfires.org/probs/ontology/data/bgs/Observation-29cc1ee823612f1307925b7c5b003feb9668a06cb991da0b6b9af30033fde2a0": "Obs 2",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation--7af16db03ac2ac2a9a773645b069b7dacffa239f5b98b9887fa4a0323b787ce7": "Obs 3",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-0cefb7bea0582e08d7878e4c3f684c2307edb305bfddd5e3ea6f3efb8f9b02c1-d92d8d1a049b5c171ed7dfde5057cddf9984bb5fdd104af98b622c1be88800a7": "Obs 1",
    "https://ukfires.org/probs/ontology/data/bgs/Observation-c2bb6910b2b19133e460750a4dd799924afd9c4aceae0736aea91635592cd1ff": "Obs 4",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-00613791c18e3cf39874c66a176e7229189e5fed28a45ef7921e3f97e9143eab-e9398b5c9aa49bcd1b2f0dc8fa74b41a9faa021848620496ad682721f2cf9a27": "Obs 5",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-00613791c18e3cf39874c66a176e7229189e5fed28a45ef7921e3f97e9143eab-e53dd7ea6154ae201c77e77a2b7260c5304cfd12b67be85965c4089720d9fa19": "Obs 6"
}
def tidydf(results):
    df = pd.DataFrame(results)
    if "Observation" in df:
        df.Observation = [obs_short_labels.get(str(x), x) for x in df.Observation]
    return df
``` -->

## Retrieve original data points

First, let's check we can retrieve the original data points consistently.
From the BGS Minerals Yearbook:

```{literalinclude} queries/original_bgs.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["original_bgs"])
```

We can also retrieve an original data point from Prodcom linked to a classification code:

```{literalinclude} queries/original_prodcom.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["original_prodcom"])
```

## Inferred observations

Now let's query for all the observations that would be relevant to modelling production of two object types, {system:ref}`CrushedStone` and {system:ref}`SandAndGravel`, in all years that are available.

```{figure} figures/Aggregates_Hierarchy_with_Obs.svg
:name: Aggregates Hierarchy with Obs

All the observations relevant to `Aggregates` components (`CrushedStone` and `SandAndGravel`).
```

Here is the SPARQL query:

```{literalinclude} queries/object_observations.rq
:language: sparql
```

And the results:

```{code-cell} ipython3
tidydf(results["object_observations"])
```

We can see where these values have come from:

```{literalinclude} queries/prov.rq
:language: sparql
```

This results in:

```{code-cell} ipython3
df = tidydf(results["prov"])
df
```

It does indeed add up to the values shown above:

```{code-cell} ipython3
df.groupby("Observation", as_index=False)["WDFValue"].sum()
```

## Further aggregation

We can further query for the aggregates observations of {system:ref}`Aggregates`:

```{literalinclude} queries/object_observations_aggregates.rq
:language: sparql
```

This results in:

```{code-cell} ipython3
tidydf(results["object_observations_aggregates"])
```

Exactly as we expected from the observations of its components:

```{figure} figures/Composition_of_Aggregates.svg
:name: Composition of Aggregates

All the observations of `Aggregates`.
```
