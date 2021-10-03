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

{doc}`As before <original_data_points>`, load the query results:

```{code-cell} ipython3
from example_data import results
```

---

Different Object instances may be used in different datasets which in fact refer to the same type of thing.

<!-- ```{literalinclude} queries/equivalence_before.rq
:language: sparql
```

```{code-cell} ipython3
results["equivalence_before"]
```

[[ Since we only have the "final" data, we also get the inferred observations derived using equivalence and composition. ]] -->

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

<!-- ```{literalinclude} queries/equivalence_after_relation.rq
:language: sparql
```

```{code-cell} ipython3
results["equivalence_after_relation"]
``` -->

```{figure} figures/EquivalenceAfter_relation.svg
:name: Equivalence of crushed stone with equivalence relation
:width: 100%

Extension of the equivalence relation.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

And we should also consider the observations inferred by {doc}`composition<composition>`.

<!-- ```{literalinclude} queries/equivalence_after_obs3.rq
:language: sparql
```

```{code-cell} ipython3
results["equivalence_after_obs3"]
```

[[ Again, since we only have the "final" data, we also get the inferred observations derived using equivalence and composition. ]] -->

```{figure} figures/EquivalenceAfter_Obs_3.svg
:name: Equivalence of crushed stone with inferred observations
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
results["equivalence_after"]
```

[[We also have additional observations derived using composition]]

```{figure} figures/EquivalenceAfter.svg
:name: Equivalence of crushed stone with inferred observations via equivalence
:width: 100%

Direct and inferred (also via equivalence) observations for `Crushed stone`, `Crushed stone in PRODCOM`, and `Crushed stone in BGS`.
```

```{figure} figures/CE-Legend_vertical.svg
:figclass: margin
:width: 80%
```

More information about equivalence in the PRObs ontology can be found [here](https://ukfires.github.io/probs-ontology).
