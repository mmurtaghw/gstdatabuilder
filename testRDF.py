import pandas as pd
from rdflib import Graph, ConjunctiveGraph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF
from io import StringIO

# Read the CSV file using pandas
df = pd.read_csv('outputData/wikidata.csv')

# Create an RDF graph using rdflib
g = ConjunctiveGraph()

# Loop over each cell in the dbpediaTriples column
for triples_string in df['dbpediaTriples']:
    # Parse the triples in the cell and add them to the graph
    try:
        # We need to convert the string of triples into a file-like object for rdflib to read from
        triples_io = StringIO(triples_string)
        g.parse(triples_io, format="n3")
    except Exception as e:
        print(f"Invalid triples in cell: {triples_string}\nError: {e}")

# Print out the number of triples in the graph
print(f"Graph contains {len(g)} triples.")
