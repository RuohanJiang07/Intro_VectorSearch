import pandas as pd

# Use the absolute path to the CSV file
df = pd.read_csv('/Users/lesliejiang/Desktop/intro_co/data/expert_profiles.csv')

# Remove duplicates based on the 'Name' column
df_unique = df.drop_duplicates(subset='Name')

# Save the cleaned dataset to a new CSV file
df_unique.to_csv('/Users/lesliejiang/Desktop/intro_co/data/expert_profiles_cleaned.csv', index=False)
