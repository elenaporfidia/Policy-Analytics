import os

import pandas as pd

from helper import generate_ts
from terms import gender_related_terms

output_dir = "./output/time_series"
os.makedirs(output_dir, exist_ok=True)

filename = "oecd_keywords_df.pkl"
df_collection = pd.read_pickle(filename)

# ------- ALL YEARS & COUNTRIES ---------
generate_ts(
    df=df_collection,
    related_terms=gender_related_terms,
    start_year=2000,
    end_year=2023,
    relevancy="gender",
    color="#4392CC",
    title="Gender-Related Terms Occurrences Over Time (2000-2023)",
    x_label="Count of Gender-Related Terms",
    y_label="Year",
    output_dir=output_dir
)

# ------- LIMITED YEAR & COUNTRIES/REGION --------
generate_ts(
    df=df_collection,
    related_terms=gender_related_terms,
    start_year=2000,
    end_year=2023,
    countries="Japan",  # Multiple countries can be given by Japan,Argentina,Australia etc.
                        # Also this format is accepted ["Japan", "Argentina", "Australia"]
                        # You can give region names as well like previously did.
                        # You can also combine region and country name as well like "America,Australia,Korea"
                        #       this will populate all the countries from America + Australia and Korea
                        #       as a list format: ["America", "Australia", "Korea"] populates same as previous
    relevancy="gender",
    color="#4392CC",
    title="Japan Gender-Related Terms Occurrences Over Time (2000-2023)",
    x_label="Count of Gender-Related Terms",
    y_label="Year",
    output_dir=output_dir
)
