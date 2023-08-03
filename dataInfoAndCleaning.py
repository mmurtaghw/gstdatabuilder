import pandas as pd

csvPath = 'outputData/wikidata.csv'

df = pd.read_csv(csvPath)

# use .head(n) to get the first n rows
print(df.head(30))

# Total number of rows and columns
print(f'Total Rows: {df.shape[0]}')
print(f'Total Columns: {df.shape[1]}')

# Information about the DataFrame including the index dtype and column dtypes, non-null values and memory usage.
df.info()

# Get a summary of the central tendencies, dispersion and shape of a dataset’s distribution, excluding NaN values.
df.describe()

# Checking for missing values
print(df.isnull().sum())

# Remove rows with NaN values
df = df.dropna()
print('After removing NaN values:')
print(df.isnull().sum())

# Checking for duplicate entries
print(f'Total Duplicates Before Dropping: {df.duplicated().sum()}')

# Dropping duplicates
df = df.drop_duplicates()

df.to_csv(csvPath)

# Checking for duplicate entries after dropping duplicates
print(f'Total Duplicates After Dropping: {df.duplicated().sum()}')
