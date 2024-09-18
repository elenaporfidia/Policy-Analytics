import re

import pandas as pd
import spacy
from tqdm import tqdm

from helper import spacy_resource, get_collection, extract_keywords

collection = get_collection()
_nlp_model = 'en_core_web_lg'

spacy_resource(_nlp_model)
nlp = spacy.load(_nlp_model)

pd_data = {
    "country": [],
    "year": [],
    "findings": [],
    "recommendations": [],
    "all": [],
    "findings_count": [],
    "recommendations_count": [],
    "all_terms_count": [],
    "year_entries": []
}

total_keywords = 0

with tqdm(total=collection.total_frs(), desc="Processing Keywords") as pbar:
    for country in collection.get_countries():
        for year in country.get_years():
            year_findings = []
            year_recommendations = []
            year_all = []
            year_entry_count = 0
            for _criteria in year.get_criteria():
                criteria_findings_keywords = []
                criteria_recommendations_keywords = []
                criteria_all_keywords = extract_keywords(nlp, _criteria.get_title())
                year_entry_count += 1
                for fr in _criteria.get_frs():
                    finding_keywords = extract_keywords(nlp, fr.get_finding())
                    recommendation_keywords = extract_keywords(nlp, fr.get_recommendation())
                    criteria_findings_keywords += finding_keywords
                    criteria_recommendations_keywords += recommendation_keywords
                    criteria_all_keywords += finding_keywords
                    criteria_all_keywords += recommendation_keywords
                    year_entry_count += 1
                    pbar.update(1)
                # -----------------------------------------
                year_findings += criteria_findings_keywords
                year_recommendations += criteria_recommendations_keywords
                year_all += criteria_all_keywords
            # ----------------------------------------------
            total_keywords += len(year_all)
            pd_data["country"].append(country.get_name())
            pd_data["year"].append(year.get_name())
            pd_data["findings"].append(" ".join(year_findings))
            pd_data["recommendations"].append(" ".join(year_recommendations))
            pd_data["all"].append(" ".join(year_all))
            pd_data["findings_count"].append(len(year_findings))
            pd_data["recommendations_count"].append(len(year_recommendations))
            pd_data["all_terms_count"].append(len(year_all))
            pd_data["year_entries"].append(year_entry_count)

filename = "oecd_keywords_df.pkl"
df = pd.DataFrame(pd_data)
df.to_pickle(filename)

print(f"Total Keyword Extracted: {total_keywords} and stored as {filename}")
