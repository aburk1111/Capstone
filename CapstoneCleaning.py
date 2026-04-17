import pandas as pd

# =========================
# EXTRACT FROM GITHUB
# =========================


base_path = "https://raw.githubusercontent.com/aburk1111/Capstone/refs/heads/main/" 
congress = pd.read_csv(base_path + "data_aging_congress.csv")
generations = pd.read_csv(base_path + "generations.csv")
life = pd.read_csv(base_path + "lifeExpectancy.csv")
party = pd.read_csv(base_path + "partyCode.csv")

# =========================
# TRANSFORM - CLEANING
# =========================

# Standardize column names (lowercase, underscores)
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

congress = clean_columns(congress)
generations = clean_columns(generations)
life = clean_columns(life)
party = clean_columns(party)


# Convert date fields
congress['start_date'] = pd.to_datetime(congress['start_date'], errors='coerce')
congress['birthday'] = pd.to_datetime(congress['birthday'], errors='coerce')

# Create year column for relationships
congress['year'] = congress['start_date'].dt.year

# Ensure consistent data types
congress['party_code'] = congress['party_code'].astype(str)
party['party_code'] = party['party_code'].astype(str)

# Trim whitespace
congress['bioname'] = congress['bioname'].str.strip()

# =========================
# DIMENSION TABLES
# =========================

# DIM PARTY
dim_party = party.drop_duplicates().copy()

# DIM GENERATION
generations.columns = generations.columns.str.strip().str.lower()
generations = generations[['year', 'generation']]
generations = generations.drop_duplicates(subset=['year']).copy()
dim_generation = generations.copy()

# DIM TIME (from congress data)
dim_time = congress[['year']].drop_duplicates().sort_values('year')
dim_time['year_key'] = dim_time['year']

# DIM LIFE EXPECTANCY
life['year'] = life['year'].astype(int)
dim_life = life.drop_duplicates().copy()

# =========================
# FACT TABLE
# =========================

fact_congress = congress.copy()
fact_congress['bioname'] = fact_congress['bioname'].str.title()

fact_congress = fact_congress[[
    'bioguide_id',
    'bioname',
    'chamber',
    'start_date',
    'state_abbrev',
    'party_code',
    'generation',
    'year',
    'age_years',
    'cmltv_cong',
    'cmltv_chamber'
]]

# Rename for clarity
fact_congress = fact_congress.rename(columns={
    'cmltv_cong': 'total_congress_terms',
    'cmltv_chamber': 'total_chamber_terms'
})

# =========================
# DATA VALIDATION
# =========================

print("Row Counts:")
print("Fact:", len(fact_congress))
print("Dim Party:", len(dim_party))
print("Dim Generation:", len(dim_generation))
print("Dim Time:", len(dim_time))
print("Dim Life:", len(dim_life))

# Check for null keys
print("\nNull Checks:")
print(fact_congress.isnull().sum())

# =========================
# LOAD (EXPORT TO CSV)
# =========================
saved_path = "C:/Capstone/"
fact_congress.to_csv(saved_path + "fact_congress.csv", index=False)
dim_party.to_csv(saved_path + "dim_party.csv", index=False)
dim_generation.to_csv(saved_path + "dim_generation.csv", index=False)
dim_time.to_csv(saved_path + "dim_time.csv", index=False)
dim_life.to_csv(saved_path + "dim_life_expectancy.csv", index=False)

print("\nETL process completed successfully.")