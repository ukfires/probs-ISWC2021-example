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

# Composition

{doc}`As before <original_data_points>`, load the query results:

```{code-cell} ipython3
from example_data import results
```

---

Often Objects can be broken down into several smaller categories.

In our data, production of `Crushed stone in BGS` is split into three smaller categories.
And there is also an Observation for the whole `Crushed stone` Object.

```{literalinclude} queries/composition_before.rq
:language: sparql
```

```{code-cell} ipython3
results["composition_before"]
```

```{figure} figures/CompositionBefore.svg
:name: Composition of crushed stone in BGS
:width: 100%

Initial observations for the components of `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

We want to know the value of `Crushed stone in BGS` obtained from its components.
We can achieve this using the PCSC "algorithm".

```{literalinclude} queries/composition_after.rq
:language: sparql
```

```{code-cell} ipython3
results["composition_after"]
```

```{figure} figures/CompositionAfter.svg
:name: Composition of crushed stone in BGS after applying the PCSC "algorithm"
:width: 100%

Direct and inferred observations for the components of `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

Note that only "compatible" observations will be aggregated.
They are "compatible" if they share the same _Role_, _Region_, _Time Period_, and _Metric_.

More information about composition in the PRObs ontology can be found [here](https://ukfires.github.io/probs-ontology).
