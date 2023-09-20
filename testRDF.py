import pandas as pd
from rdflib import Graph, ConjunctiveGraph
from io import StringIO

# Read the CSV file using pandas
df = pd.read_csv('outputData/wikidataFiltered.csv')

# Create an RDF graph using rdflib
g = ConjunctiveGraph()

# Initialize the count of valid and invalid n-triple sets
valid_count = 0
invalid_count = 0

# Create a list to store rows with valid triples
valid_rows = []

def sanitize_triples(triples_string):
    # Replace newline characters and escaped characters for quotes
    sanitized = triples_string.replace('\n', ' ').replace('\\"', '"').replace("\\'", "'")
    # Ensure each statement ends with a '.'
    sanitized = sanitized.rstrip('.')
    sanitized += ' .'
    return sanitized

# Loop over each cell in the dbpediaTriples column
for index, row in df.iterrows():
    triples_string = row['dbpediaTriples']
    
    # Sanitize the triples_string to handle newlines within literals
    sanitize_triples(triples_string)
    
    # Parse the triples in the cell and add them to the graph
    try:
        # Convert the string of triples into a file-like object for rdflib
        triples_io = StringIO(triples_string)
        g.parse(triples_io, format="n3")
        valid_count += 1
        valid_rows.append(row)
    except Exception as e:
        print(f"Invalid triples in cell at index {index}:\nError: {e}")
        invalid_count += 1

# Concatenate all valid rows into a new DataFrame only if there are valid rows
if valid_rows:
    valid_df = pd.concat(valid_rows, axis=1).transpose()
    # Save the DataFrame with only valid triples to a new CSV file
    valid_df.to_csv('outputData/validTriples.csv', index=False)
else:
    print("No valid triples found to concatenate.")

# Print out the number of triples in the graph
print(f"Graph contains {len(g)} triples.")

# Print out the count of valid and invalid n-triple sets
print(f"Number of valid n-triple sets: {valid_count}")
print(f"Number of invalid n-triple sets: {invalid_count}")
