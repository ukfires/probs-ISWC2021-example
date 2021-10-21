Processing pipeline
===================

In the back-end, the following pipeline is executed:

```{figure} figures/Pipeline.svg
:name: pipeline
:width: 100%

Back-end pipeline of the PRObs system. The rectangles represent the steps of our pipeline (<strong style="color:#b3deb8">green</strong> for Python scripts and <strong style="color:#b3c5e8">blue</strong> for RDFox scripts). The ellipses represent inputs and outputs (dashed for internal results).
```

We first run some preprocessing steps to transform the data and the ontology into a format that is more compatible with RDFox. Then we load the datasets and the ontologies, and we run the 'Conversion' phase to convert the data into RDF, enrich them with new information (for instance, the new inferred _Observations_ from equivalence and composition), and save them. Finally, in the 'Reasoning' phase the whole PRObs Knowledge Graph is loaded and a SPARQL endpoint is exposed to answer queries over it.
