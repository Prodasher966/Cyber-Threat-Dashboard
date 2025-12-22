import pandas as pd

# Load the CSV file
df = pd.read_csv('Global_Cybersecurity_Threats_2015-2024.csv')

# Get the column names and their data types
column_types = df.dtypes

# Print the column names and their types
print(column_types)
