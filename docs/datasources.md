# Data sources

Three data sources are used in this example analysis: Prodcom, Comtrade, and the British Geological Survey Minerals Yearbook.

## Prodcom
    
The [Prodcom](https://ec.europa.eu/eurostat/web/prodcom) database provides statistics on the production of goods and materials within the EU, published by Eurostat. The data is organised according the [PRODCOM list](https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM&StrGroupCode=CLASSIFIC&StrLanguageCode=EN&IntFamilyCode=&TxtSearch=prodcom&IntCurrentPage=1) classification system, and includes both physical production (e.g. by mass or by volume) and the economic value of the goods sold.

To access this data, we [load the classification system into RDFox](https://github.com/ukfires/probs-ontology-example/blob/master/datasources/prodcom/load_data.rdfox#L1-L79) and [map it into RDF](https://github.com/ukfires/probs-ontology-example/blob/master/datasources/prodcom/map.dlog). This creates {term}`Object`s for every classification code item, named `PRODCOM Object from Code XXXXXXXX`.

The data for each classification code is then [loaded similarly](https://github.com/ukfires/probs-ontology-example/blob/master/datasources/prodcom/load_data.rdfox#L81-L154) and [mapped](https://github.com/ukfires/probs-ontology-example/blob/master/datasources/prodcom/map.dlog) to create {term}`DirectObservation`s corresponding to each classification code.

See {doc}`query_results` for example query results showing how the raw data is retrieved as RDF.

```{note}
For illustrative purposes, two pieces of Prodcom data have been removed from the 2018 dataset (codes `08.12.11.90` and `08.12.12.10`, corresponding to "sand & gravel" in the later example). This is done firstly to simplify the number of inferred observations, and secondly to include an incomplete lower-bound observation in the results.
```

## Comtrade

The [UN Comtrade database](https://comtrade.un.org) provides statistics on international trade. The data is classificed according to the [Harmonized System](https://unstats.un.org/unsd/tradekb/Knowledgebase/50018/Harmonized-Commodity-Description-and-Coding-Systems-HS) classification codes.

The Comtrade classification codes and data are loaded and mapped analogously to Prodcom, as described above (see [datasources/comtrade](https://github.com/ukfires/probs-ontology-example/tree/master/datasources/comtrade)).

## BGS Minerals Yearbook

The [British Geological Survey Minerals Yearbook](https://www2.bgs.ac.uk/mineralsuk/download/ukmy/UKMY2015.pdf) contains data tables for production of various minerals. Since unlike Prodcom and Comtrade they are not linked to a systematic classification, we need to define the dataset-specific {term}`Object`s that appear in the data, which will be mapped onto the equivalent reference object names that our model would like to use (defined in {doc}`object_definitions`).

```{system:object} BGSCrushedStone
:label: Crushed stone in BGS
:become_parent: true

This is the *composite* object for all of crushed stone.
```

Crushed stone can be further classified into the following components, which are linked to `BGSCrushedStone` with `:objectComposedOf`:

```{system:object} BGSLimestoneAndDolomite
:label: Limestone & Dolomite in BGS
```

```{system:object} BGSIgneousRock
:label: Igneous rock in BGS
```

```{system:object} BGSSandstone
:label: Sandstone in BGS
```

```{end-sub-objects}
```

The table also includes production of sand and gravel:

```{system:object} BGSSandAndGravel
:label: Sand & Gravel in BGS
```
