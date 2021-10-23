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

# Aggregates

{doc}`As before <original_data_points>`, load the query results:

```{code-cell} ipython3
from example_data import results
```

---

## Inferred observations

Let's query for all the observations that would be relevant to modelling production of two object types, {system:ref}`CrushedStone` and {system:ref}`SandAndGravel`, in all years that are available.

```{figure} figures/Aggregates_Hierarchy_with_Obs.svg
:name: Aggregates Hierarchy with Obs
:width: 100%

All the observations relevant to `Aggregates` components (`CrushedStone` and `SandAndGravel`).
```

Here is the SPARQL query:

```{literalinclude} queries/object_observations.rq
:language: sparql
```

And the results:

```{code-cell} ipython3
results["object_observations"]
```

We can see where these values have come from:

```{literalinclude} queries/prov.rq
:language: sparql
```

This results in:

```{code-cell} ipython3
results["prov"]
```

It does indeed add up to the values shown above:

```{code-cell} ipython3
results["prov"].groupby("Observation", as_index=False)["WDFValue"].sum()
```

## Further aggregation

We can further query for the aggregates observations of {system:ref}`Aggregates`:

```{literalinclude} queries/object_observations_aggregates.rq
:language: sparql
```

This results in:

```{code-cell} ipython3
results["object_observations_aggregates"]
```

Exactly as we expected from the observations of its components:

```{figure} figures/Composition_of_Aggregates.svg
:name: Composition of Aggregates
:width: 100%

All the observations of `Aggregates`.
```
