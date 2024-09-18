import os

import pandas as pd

from helper import generate_category_chart

output_dir = "./output/categories_charts"
os.makedirs(output_dir, exist_ok=True)

filename = "oecd_keywords_df.pkl"
df_collection = pd.read_pickle(filename)

# --------- EUROPE ---------
generate_category_chart(
    start_year=2000,
    end_year=2010,
    countries="Europe",
    output_dir=output_dir,
    df=df_collection
)

generate_category_chart(
    start_year=2011,
    end_year=2023,
    countries="Europe",
    output_dir=output_dir,
    df=df_collection
)

# --------- ASIA ---------
generate_category_chart(
    start_year=2000,
    end_year=2010,
    countries="Asia",
    output_dir=output_dir,
    df=df_collection
)

generate_category_chart(
    start_year=2011,
    end_year=2023,
    countries="Asia",
    output_dir=output_dir,
    df=df_collection
)

# --------- AMERICA ---------
generate_category_chart(
    start_year=2000,
    end_year=2010,
    countries="America",
    output_dir=output_dir,
    df=df_collection
)

generate_category_chart(
    start_year=2011,
    end_year=2023,
    countries="America",
    output_dir=output_dir,
    df=df_collection
)

# -------- for SINGLE or MULTIPLE countries/region --------
generate_category_chart(
    start_year=2000,
    end_year=2010,
    countries="Japan",  # Multiple countries can be given by Japan,Argentina,Australia etc.
                        # Also this format is accepted ["Japan", "Argentina", "Australia"]
                        # You can give region names as well like previously did.
                        # You can also combine region and country name as well like "America,Australia,Korea"
                        #       this will populate all the countries from America + Australia and Korea
                        #       as a list format: ["America", "Australia", "Korea"] populates same as previous
    output_dir=output_dir,
    df=df_collection
)

generate_category_chart(
    start_year=2011,
    end_year=2023,
    countries="Japan",
    output_dir=output_dir,
    df=df_collection
)

