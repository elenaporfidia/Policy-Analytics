import os

import pandas as pd

from helper import nltk_resources, create_word_cloud

nltk_resources([
    'corpora/stopwords',
    'tokenizers/punkt',
    'corpora/wordnet',
    'taggers/averaged_perceptron_tagger',
    'chunkers/maxent_ne_chunker',
    'corpora/words'
])

# Change dir as you required
output_dir = "./output/word_clouds"
os.makedirs(output_dir, exist_ok=True)

filename = "oecd_keywords_df.pkl"
df_collection = pd.read_pickle(filename)

# ---------------  RECOMMENDATIONS  ----------------------------
create_word_cloud(
    df=df_collection,
    start_year=2000,
    end_year=2010,
    column="recommendations",
    color="blue",
    title="Recommendations Word Cloud (2000-2010)",
    output_dir=output_dir
)

create_word_cloud(
    df=df_collection,
    start_year=2011,
    end_year=2023,
    column="recommendations",
    color="orange",
    title="Recommendations Word Cloud (2011-2023)",
    output_dir=output_dir
)

# ----------------  FINDINGS  ---------------------------
create_word_cloud(
    df=df_collection,
    start_year=2000,
    end_year=2010,
    column="findings",
    color="blue",
    title="Findings Word Cloud (2000-2010)",
    output_dir=output_dir
)
create_word_cloud(
    df=df_collection,
    start_year=2011,
    end_year=2023,
    column="findings",
    color="orange",
    title="Findings Word Cloud (2011-2023)",
    output_dir=output_dir
)

# ---------------  ALL  ----------------------------
create_word_cloud(
    df=df_collection,
    start_year=2000,
    end_year=2010,
    column="all",
    color="blue",
    title="Word Cloud (2000-2010)",
    output_dir=output_dir
)
create_word_cloud(
    df=df_collection,
    start_year=2011,
    end_year=2023,
    column="all",
    color="orange",
    title="Word Cloud (2011-2023)",
    output_dir=output_dir
)

# ----  COUNTRY/REGION BASED WORD CLOUD  -------------
create_word_cloud(
    df=df_collection,
    start_year=2011,
    end_year=2023,
    countries="Japan",  # Multiple countries can be given by Japan,Argentina,Australia etc.
                        # Also this format is accepted ["Japan", "Argentina", "Australia"]
                        # You can give region names as well like previously did.
                        # You can also combine region and country name as well like "America,Australia,Korea"
                        #       this will populate all the countries from America + Australia and Korea
                        #       as a list format: ["America", "Australia", "Korea"] populates same as previous
    column="all",
    color="orange",
    title="Word Cloud (2011-2023)",
    output_dir=output_dir
)