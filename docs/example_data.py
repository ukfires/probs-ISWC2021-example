"""Helper code to query and tidy up results."""

from pathlib import Path
import pandas as pd
from rdflib import URIRef, Namespace
from rdflib.namespace import RDF, RDFS

from probs_runner import probs_query_data, PROBS

# Load the SPARQL queries from the text files
queries = {
    p.stem: p.read_text()
    for p in Path("queries").glob("*.rq")
}

# Start RDFox with the given data file, and connect to the endpoint to answer
# the SPARQL queries.
original_results = probs_query_data("../data/probs_data.nt.gz", queries)

# Do a bit of tidying up so the results are easier to read.
obs_short_labels = {
    "https://ukfires.org/probs/ontology/data/bgs/Observation-29cc1ee823612f1307925b7c5b003feb9668a06cb991da0b6b9af30033fde2a0": "Obs 2",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation--7af16db03ac2ac2a9a773645b069b7dacffa239f5b98b9887fa4a0323b787ce7": "Obs 3",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-0cefb7bea0582e08d7878e4c3f684c2307edb305bfddd5e3ea6f3efb8f9b02c1-d92d8d1a049b5c171ed7dfde5057cddf9984bb5fdd104af98b622c1be88800a7": "Obs 1",
    "https://ukfires.org/probs/ontology/data/bgs/Observation-c2bb6910b2b19133e460750a4dd799924afd9c4aceae0736aea91635592cd1ff": "Obs 4",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-00613791c18e3cf39874c66a176e7229189e5fed28a45ef7921e3f97e9143eab-e9398b5c9aa49bcd1b2f0dc8fa74b41a9faa021848620496ad682721f2cf9a27": "Obs 5",
    "https://ukfires.org/probs/ontology/ComposedInferredObservation-prodcom/2017/Object-00613791c18e3cf39874c66a176e7229189e5fed28a45ef7921e3f97e9143eab-e53dd7ea6154ae201c77e77a2b7260c5304cfd12b67be85965c4089720d9fa19": "Obs 6",
    "https://ukfires.org/probs/ontology/data/bgs/Observation-59b0bb2c5ac81e0a4f8065cede30db3ac72adac049383c1f95204c354fe76459": "Obs A",
    "https://ukfires.org/probs/ontology/data/bgs/Observation-897e20a96c17d017a9142d1fd4832df34cca88a8920db5156611d05ff4b5775f": "Obs B",
    "https://ukfires.org/probs/ontology/data/bgs/Observation-2cc32f0cec07ace893b51a0e546f74ca6bc2f7f91f467e4b1fa3e73da9562884": "Obs C",

}

NAMESPACES = {
    "sys": Namespace("http://ukfires.org/probs/system/"),
    "": PROBS,
    "rdf": RDF,
    "rdfs": RDFS,
    "quantitykind": Namespace("http://qudt.org/vocab/quantitykind/"),
}


def replace_prefixes(x):
    if isinstance(x, URIRef):
        for k, v in NAMESPACES.items():
            if x.startswith(str(v)):
                return f"{k}:{x[len(v):]}"
    return x


def tidydf(results):
    df = pd.DataFrame(results)

    # Use abbreviated names for the specific observations, to match the paper
    if "Observation" in df:
        df.Observation = [obs_short_labels.get(str(x), x) for x in df.Observation]
    if "WDF" in df:
        df.WDF = [obs_short_labels.get(str(x), x) for x in df.WDF]
    if "Year" in df:
        df.Year = [x.year for x in df.Year]

    # Use SPARQL prefixes
    df = df.applymap(replace_prefixes)

    return df

# These are the tidied results we will show in the jupyter book page
results = {
    k: tidydf(v) for k, v in original_results.items()
}
