import pandas as pd

# Load the first table
table1 = pd.read_excel('Table1.xlsx')

# Load the second table
table2 = pd.read_excel('Table2.xlsx')

# Combine the two tables
result = pd.concat([table1, table2], sort=False)

# Drop duplicate rows based on the first column (assumed to be datetime data)
result = result.drop_duplicates(subset=[result.columns[0]])

# Save the combined and deduplicated data to a new file
result.to_excel('Combined_Tables.xlsx', index=False)
