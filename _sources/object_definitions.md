---
jupytext:
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

Object definitions
==================

{doc}`As before <original_data_points>`, load the query results:

```{code-cell} ipython3
from example_data import results
```

---

Here are just a few example object types which we might be interested in modelling.

```{system:object} Aggregates
:become_parent: true
```

```{system:object} CrushedStone
:label: Crushed stone
```

```{system:object} SandAndGravel
:label: Sand & Gravel
```

```{end-sub-objects}
```

```{figure} figures/Aggregates_Hierarchy.svg
:name: Aggregates Hierarchy
:width: 100%

Aggregates Hierarchy.
```

Note that these are "new" objects that we have created because they are interesting for our analysis.
We also call them _Reference Objects_.

We can retrieve them using the following query:

```{literalinclude} queries/object_definitions.rq
:language: sparql
```

```{code-cell} ipython3
results["object_definitions"]
```

And we can see the components of `Aggregates` with this query:

```{literalinclude} queries/object_definitions_composition.rq
:language: sparql
```

```{code-cell} ipython3
results["object_definitions_composition"]
```
