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

# Equivalence

## Behind-the-scenes

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

```{code-cell} ipython3
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
```

---

Different Object instances may be used in different datasets which in fact refer to the same type of thing.

```{literalinclude} queries/equivalence_before.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["equivalence_before"])
```

```{figure} figures/EquivalenceBefore.svg
:name: Equivalence of crushed stone
:width: 100%

Initial observations for `Crushed stone`, `Crushed stone in PRODCOM`, and `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

To allow querying of observations in an uniform way, we want to propagate the observation to all the equivalent objects.

First, this is an equivalence relation (it is reflexive, symmetric, and transitive).

```{literalinclude} queries/equivalence_after_relation.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["equivalence_after_relation"])
```

```{figure} figures/EquivalenceAfter_relation.svg
:name: Equivalence of crushed stone
:width: 100%

Extension of the equivalence relation.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

And we should also consider the observations inferred by composition.
[[Add link to composition page]]

```{literalinclude} queries/equivalence_after_obs3.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["equivalence_after_obs3"])
```

```{figure} figures/EquivalenceAfter_Obs_3.svg
:name: Equivalence of crushed stone
:width: 100%

Direct and inferred observations for `Crushed stone`, `Crushed stone in PRODCOM`, and `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

We want to propagate observations among all the equivalent objects avoiding duplication.

```{literalinclude} queries/equivalence_after.rq
:language: sparql
```

```{code-cell} ipython3
tidydf(results["equivalence_after"])
```

```{figure} figures/EquivalenceAfter.svg
:name: Equivalence of crushed stone
:width: 100%

Direct and inferred (also via equivalence) observations for `Crushed stone`, `Crushed stone in PRODCOM`, and `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

More information about equivalence in the PRObs ontology can be found [here](https://ukfires.github.io/probs-ontology).
