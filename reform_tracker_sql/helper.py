import os
import pickle
import re
import string
import subprocess
import sys
import zipfile
from urllib.parse import urlsplit

import pandas as pd
from wordcloud import WordCloud
import nltk
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.data import find

import requests
import spacy
from tqdm import tqdm
from typer.colors import BLUE

from entities.Collection import Collection
from entities.Country import Country
from entities.Criteria import Criteria
from entities.FindingRecommendation import FindingRecommendation
from entities.Year import Year
from terms import economic_reform_terms, environmental_policy_terms, social_policy_terms, gender_related_terms

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DBAPIError
from models.Connection import getSession
from models.CountryModel import CountryModel
from models.YearModel import YearModel
from models.CountryYearCriteriaModel import CountryYearCriteriaModel
from models.FindingRecommendationModel import FindingRecommendationModel
from models.CriteriaModel import CriteriaModel

_stop_words = set(stopwords.words("english"))
additional_stop_words = {
    "government",
    "recommendation",
    "finding",
    "policy",
    "public",
    "economy",
    "economic",
    "growth",
    "increase",
    "reduce",
    "implement",
    "reform",
    "improve",
    "system",
    "cost",
    "support",
    "high",
    "low",
    "risk",
    "ensure",
    "maintain",
    "continue",
    "develop",
    "service",
    "new",
    "programme",
    "spending",
    "sector",
    "price",
    "level",
    "bank",
    "fiscal",
    "monetary",
    "inflation",
    "competition",
    "firm",
    "long",
    "term",
    "year",
    "present",
    "ha",
    "small",
    "large",
    "market",
    "potential",
    "one",
    "great",
    "greater",
    "lower",
    "third",
    "job",
    "employment",
    "governance",
    "achieve",
    "training",
    "many",
    "challenge",
    "central",
    "use",
    "rate",
    "pay",
    "likely",
    "tax",
    "currency",
    "special",
    "labour",
    "lack",
    "social",
    "allow",
    "scheme",
    "personal",
    "time",
    "income",
    "base",
    "exemption",
    "rule",
    "severe",
    "misconduct",
    "governor",
    "financial",
    "target",
    "extend",
    "keep",
    "content",
    "active",
    "barrier",
    "early",
    "scale",
    "rigid",
    "benefit",
    "wa",
    "imf",
    "share",
    "additional",
    "undermine",
    "regime",
    "individual",
    "undertake",
    "dismissal",
    "limit",
    "adhere",
    "provincial",
    "general",
    "entry",
    "formal",
    "administrative",
    "condition",
    "office",
    "impact",
    "drop",
    "informal",
    "force",
    "capital",
    "reversal",
    "unfair",
    "operate",
    "currently",
    "smaller",
    "bolster",
    "vocational",
    "merge",
    "non",
    "input",
    "wide",
    "intermediate",
    "rationalise",
    "province",
    "review",
    "pursue",
    "surprise",
    "vet",
    "regulatory",
    "temporary",
    "direction",
    "remove",
    "operational",
    "reduction",
    "space",
    "line",
    "transfer",
    "deteriorate",
    "indicator",
    "deduction",
    "temporarily",
    "adequate",
    "type",
    "alt",
    "transfer",
    "line",
    "raise",
    "need",
    "remain",
    "measure",
    "include",
    "introduce",
    "private",
    "country",
    "state",
    "finance",
    "consider",
    "housing",
    "quality",
    "relatively",
    "worker",
    "local",
    "address",
    "well",
    "current",
    "oecd",
    "access",
    "gdp",
    "student",
    "teacher",
    "plan",
    "japan",
    "australia",
    "argentina"
}
_stop_words.update(additional_stop_words)
_stop_words.discard("present")


def nltk_resource_exists(resource):
    try:
        find(resource)
        return True
    except LookupError:
        return False


def nltk_resumed_download(resource_url, download_path):
    if os.path.exists(download_path):
        resume_header = {'Range': f'bytes={os.path.getsize(download_path)}-'}
        mode = 'ab'
    else:
        resume_header = {}
        mode = 'wb'

    response = requests.get(resource_url, headers=resume_header, stream=True)
    response.raise_for_status()
    content_length = response.headers.get('content-length')
    total_size = int(content_length) if content_length else None
    if os.path.exists(download_path):
        total_size += os.path.getsize(download_path)

    with open(download_path, 'wb') as file, tqdm(
            desc="",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            colour=BLUE
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))


def nltk_download_resource(resource, retry=3):
    base_url = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/"
    resource_url = base_url + resource + ".zip"
    download_path = os.path.join(nltk.data.path[0], resource + ".zip")
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    try:
        for attempt in range(retry):
            try:
                nltk_resumed_download(resource_url, download_path)
                break
            except Exception as e:
                if attempt < retry - 1:
                    pass
                else:
                    if os.path.exists(download_path):
                        os.remove(download_path)
                    raise

        if os.path.exists(download_path):
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.testzip()
                zip_ref.extractall(os.path.dirname(download_path))
        else:
            sys.exit()

    except requests.RequestException as e:
        print(f"Failed to download {resource}: {e}")
    except zipfile.BadZipFile:
        print(f"Downloaded file for {resource} is not a valid ZIP file.")
    finally:
        if os.path.exists(download_path):
            os.remove(download_path)


def nltk_resources(resources):
    for resource in resources:
        if not nltk_resource_exists(resource):
            print(f"Downloading {resource}:")
            nltk_download_resource(resource)
            print("\n")


def spacy_get_model_info(model):
    base_url = "https://api.github.com/repos/explosion/spacy-models/releases"
    response = requests.get(base_url)
    releases = response.json()
    for release in releases:
        assets = release.get('assets', [])
        for asset in assets:
            if model in asset['name']:
                return {
                    'url': asset['browser_download_url'],
                    'version': release['tag_name']
                }
    raise ValueError(f"Spacy Model '{model}' not found in the releases.")


def spacy_resumed_download(url, file_name, model):
    if not file_name:
        return

    if os.path.exists(file_name):
        resume_header = {'Range': f'bytes={os.path.getsize(file_name)}-'}
        mode = 'ab'
    else:
        resume_header = {}
        mode = 'wb'

    response = requests.get(url, headers=resume_header, stream=True)
    response.raise_for_status()
    content_length = response.headers.get('content-length')
    total_size = int(content_length) if content_length else None
    if os.path.exists(file_name):
        total_size += os.path.getsize(file_name)
    with open(file_name, mode) as file, tqdm(
            desc="",
            total=total_size,
            initial=os.path.getsize(file_name) if os.path.exists(file_name) else 0,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            colour=BLUE
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))


def spacy_download_model(model, retry=3):
    try:
        model_info = spacy_get_model_info(model)
        download_url = model_info['url']
        file_name = os.path.basename(urlsplit(download_url).path)
        for attempt in range(retry):
            try:
                spacy_resumed_download(download_url, file_name, model)
                break
            except Exception as e:
                if attempt < retry - 1:
                    pass
                else:
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    raise

        if os.path.exists(file_name):
            print(f"Installing the spacy model {model}...")
            subprocess.run([sys.executable, "-m", "pip", "install", file_name], check=True)
            os.remove(file_name)
        else:
            sys.exit()
    except Exception as e:
        print(f"An error occurred while downloading and installing the spacy model: {model}\n {e}")


def spacy_resource(resource):
    try:
        spacy.load(resource)
    except OSError:
        print(f"Downloading Spacy Model {resource}:")
        spacy_download_model(resource)


def get_collection():
    total_entries = getNumberOfEntries()
    countries = getCountryYearCriteriaWiseFindingRecommendation(total_entries)
    collections = Collection([])

    for ci, country in countries.items():
        _country = Country(country["id"], country["name"], [])
        for yi, year in country["years"].items():
            _year = Year(year["id"], year["name"], [])
            for cri, criteria in year["criteria"].items():
                _criteria = Criteria(criteria["id"], criteria["title"], [])
                for fri, finding_recommendation in criteria["findings_recommendations"].items():
                    _finding_recommendation = FindingRecommendation(
                        finding_recommendation["id"],
                        finding_recommendation["finding"],
                        finding_recommendation["recommendation"]
                    )
                    _criteria.frs.append(_finding_recommendation)
                _year.criteria.append(_criteria)
            _country.years.append(_year)
        collections.countries.append(_country)

    return collections


def extract_keywords(_nlp, text):
    excluded_tags = {"DET", "ADP", "CCONJ", "SCONJ"}
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<!\s\.\s)[.!?]\s+', text)
    punctuation_and_symbols = set(string.punctuation)
    all_keywords = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            doc = _nlp(sentence)
            keywords = [
                token.lemma_.lower() for token in doc
                if token.pos_ not in excluded_tags
                   and token.lemma_.lower() not in _stop_words
                   and not token.text.endswith(("ing", "en", "ed", "ly", "ry", "es"))
                   and not token.is_stop
                   and token.text not in punctuation_and_symbols
                   and not token.text.isdigit()
                   and not re.match(r'^[\[\]{}()<>]$', token.text)
            ]
            keywords = [keyword.lower() for keyword in keywords]
            all_keywords.append(keywords)

    return [item for sublist in all_keywords for item in sublist]


def cloud_color(**kwargs):
    colors = {
        "blue": "27, 102, 167",
        "orange": "154, 46, 10"
    }

    frequency = kwargs.get('frequency', 1)
    max_freq = kwargs.get('max_frequency', 1)
    color = kwargs.get('color', "blue")
    alpha = max(0.1, frequency / max_freq)
    return rgba_to_hex(f"{colors[color]}, {alpha}")


def rgba_to_hex(color):
    color = color.strip().replace(' ', '').lower().split(",")
    r, g, b, a = [int(item) for item in color[:-1]] + [float(color[-1])]
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    a = max(0.0, min(a, 1.0))
    r = int(r * a + 255 * (1 - a))
    g = int(g * a + 255 * (1 - a))
    b = int(b * a + 255 * (1 - a))
    return f'#{r:02X}{g:02X}{b:02X}'


def create_word_cloud(df, column, color, title, output_dir, start_year, end_year, countries=None):
    global _stop_words
    text = filter_df_for_wc(df, column, start_year, end_year, countries)
    filename = os.path.join(output_dir, get_wc_filename(column, start_year, end_year, countries))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    frequency = wordcloud.process_text(text)
    max_frequency = max(frequency.values(), default=1)
    wordcloud = WordCloud(
        max_font_size=250,
        min_font_size=10,
        width=1920,
        height=1080,
        stopwords=_stop_words,
        background_color="white",
        color_func=lambda word, font_size, position, orientation, random_state=None, **kwargs: cloud_color(
            color=color,
            frequency=frequency.get(word, 1),
            max_frequency=max_frequency
        ),
    ).generate(text)
    plt.figure(figsize=(9, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(title)
    plt.axis("off")
    plt.savefig(filename, dpi=600)
    plt.close()
    print(f"Saved as: {filename}")


def show_ts_plot(x, y, color, title, xlabel, ylabel, figsize, filename):
    plt.figure(figsize=figsize)
    plt.plot(y, x, color)
    plt.title(title)
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    print(f"Saved as: {filename}")


def count_terms(text, related_terms):
    count = 0
    for term in related_terms:
        count += text.lower().count(term)
    return count


def process_ts_frequency(df, related_terms, start_year, end_year, countries=None, dp=2):
    # dp for maximum decimal position
    df_filtered = filter_df_for_ts(df, start_year, end_year, countries)
    df_filtered.loc[df_filtered.index, "relevant_term_count"] = df_filtered.apply(
        lambda row: count_terms(row["all"], related_terms),
        axis=1
    )
    df_filtered = df_filtered[["country", "year", "all_terms_count", "year_entries", "relevant_term_count"]]
    df_filtered["trend_terms"] = (
            (df_filtered["relevant_term_count"] / df_filtered["year_entries"]).round(dp) * pow(10, dp)
    ).astype(int)
    yearly_terms_count = df_filtered.groupby("year")["trend_terms"].sum().reset_index(name="term_count")
    yearly_document_count = df_filtered.groupby("year")["country"].size().reset_index(name="document_count")
    yearly_trends = pd.merge(yearly_terms_count, yearly_document_count, on="year")
    yearly_trends["trends"] = (
        (yearly_trends["term_count"] / yearly_trends["document_count"]).round(dp)
    ).astype(int)
    series_data = yearly_trends[["year", "trends"]]
    series_data.loc[:, "year"] = series_data["year"].astype(int)
    return series_data


def generate_ts(df, related_terms, color, title, x_label, y_label, output_dir,
                start_year, end_year, relevancy, countries=None, dp=2, figsize=(12, 6)):
    series_data = process_ts_frequency(df, related_terms, start_year, end_year, countries, dp)
    filename = get_ts_filename(relevancy, start_year, end_year, countries)
    filename = os.path.join(output_dir, filename)
    show_ts_plot(series_data["trends"], series_data["year"], color, title, x_label, y_label, figsize, filename)


def get_chart_filename(start_year, end_year, countries=None):
    def clean_name(name):
        return re.sub(r'[^\w]', '_', name).lower()

    if not countries:
        return f"rc_{start_year}_{end_year}.png"

    if isinstance(countries, list):
        countries = [clean_name(countries[0])] + [clean_name(countries[-1])] if len(countries) > 1 else [
            clean_name(countries[0])]
    else:
        countries = [clean_name(countries.strip().split(',')[0]),
                     clean_name(countries.strip().split(',')[-1])] if ',' in countries else [clean_name(countries)]

    return f"rc_{start_year}_{end_year}_{'_'.join(countries)}.png"


def get_ts_filename(relevancy, start_year, end_year, countries=None):
    def clean_name(name):
        return re.sub(r'[^\w]', '_', name).lower()

    if not countries:
        return f"ts_{relevancy}_terms_{start_year}_{end_year}.png"

    if isinstance(countries, list):
        countries = [clean_name(countries[0])] + [clean_name(countries[-1])] if len(countries) > 1 else [
            clean_name(countries[0])]
    else:
        countries = [clean_name(countries.strip().split(',')[0]),
                     clean_name(countries.strip().split(',')[-1])] if ',' in countries else [clean_name(countries)]

    return f"ts_{relevancy}_terms_{start_year}_{end_year}_{'_'.join(countries)}.png"


def get_wc_filename(column, start_year, end_year, countries=None):
    def clean_name(name):
        return re.sub(r'[^\w]', '_', name).lower()

    if not countries:
        return f"{column}_wordcloud_{start_year}_{end_year}.png"

    if isinstance(countries, list):
        countries = [clean_name(countries[0])] + [clean_name(countries[-1])] if len(countries) > 1 else [
            clean_name(countries[0])]
    else:
        countries = [clean_name(countries.strip().split(',')[0]),
                     clean_name(countries.strip().split(',')[-1])] if ',' in countries else [clean_name(countries)]

    return f"{column}_wordcloud_{start_year}_{end_year}_{'_'.join(countries)}.png"


def extract_countries(countries=None):
    regions = {
        'Europe': [
            'Estonia', 'Latvia', 'Lithuania', 'Belgium', 'Croatia', 'Czech Republic',
            'Euro Area', 'France', 'Germany', 'Hungary', 'Ireland', 'Luxembourg',
            'Netherlands', 'Norway', 'Poland', 'Portugal', 'Russian Federation',
            'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom'
        ],
        'Asia': [
            'China', 'Indonesia', 'Japan', 'Korea', 'Malaysia', 'Türkiye',
            'Viet Nam'
        ],
        'America': [
            'Argentina', 'Brazil', 'Colombia', 'Costa Rica', 'Mexico', 'United States'
        ]
    }

    if not countries:
        return countries

    if isinstance(countries, str):
        countries = [country.strip() for country in countries.split(',')]

    return [
        country for item in countries for country in (
            regions.get(item, [item]) if item in regions else [item]
        )
    ]


def calculate_terms_in_category(df_filtered, related_terms, dp=2):
    df_filtered.loc[df_filtered.index, "relevant_term_count"] = df_filtered.apply(
        lambda row: count_terms(row["recommendations"], related_terms),
        axis=1
    )
    df_filtered = df_filtered[
        ["country", "year", "recommendations_count", "year_entries", "relevant_term_count"]
    ].copy()
    df_filtered.loc[df_filtered.index, "trend_terms"] = (
            (df_filtered["relevant_term_count"] / df_filtered["year_entries"]).round(dp) * pow(10, dp)
    ).astype(int)
    yearly_terms_count = df_filtered.groupby("year")["trend_terms"].sum().reset_index(name="term_count")
    yearly_document_count = df_filtered.groupby("year")["country"].size().reset_index(name="document_count")
    yearly_trends = pd.merge(yearly_terms_count, yearly_document_count, on="year")
    yearly_trends["trends"] = (
        (yearly_trends["term_count"] / yearly_trends["document_count"]).round(dp)
    ).astype(int)

    return yearly_trends["term_count"].sum()


def filter_df_for_ts(df, start_year, end_year, countries=None):
    filtered_df = df[(df['year'].astype(int) >= start_year) & (df['year'].astype(int) <= end_year)]
    countries = extract_countries(countries)

    if countries:
        filtered_df = filtered_df[filtered_df["country"].isin(countries)]

    return filtered_df.copy()


def filter_df_for_wc(df, column, start_year, end_year, countries=None):
    filtered_df = df[(df['year'].astype(int) >= start_year) & (df['year'].astype(int) <= end_year)]
    countries = extract_countries(countries)

    if countries:
        filtered_df = filtered_df[filtered_df["country"].isin(countries)]

    return " ".join(filtered_df[column])


def filter_df_for_cc(df, start_year, end_year, countries=None):
    filtered_df = df[(df['year'].astype(int) >= start_year) & (df['year'].astype(int) <= end_year)]
    countries = extract_countries(countries)

    if countries:
        filtered_df = filtered_df[filtered_df["country"].isin(countries)]

    return filtered_df


def generate_category_chart(df, start_year, end_year, output_dir, countries=None):
    filtered_df = filter_df_for_cc(df, start_year, end_year, countries)

    _category = {
        'category': ['economic reforms', 'environmental policies', 'social policies', 'gender'],
        'term_count': [
            calculate_terms_in_category(filtered_df.copy(), economic_reform_terms),
            calculate_terms_in_category(filtered_df.copy(), environmental_policy_terms),
            calculate_terms_in_category(filtered_df.copy(), social_policy_terms),
            calculate_terms_in_category(filtered_df.copy(), gender_related_terms)
        ]
    }

    output_file = os.path.join(output_dir, get_chart_filename(start_year, end_year, countries))

    plt.figure(figsize=(10, 9))
    plt.barh(_category['category'], _category['term_count'], color='#81BE37')
    plt.xlabel('Frequency')
    plt.title(f'Recommendations Categorization for {start_year}-{end_year}')
    plt.gca().invert_yaxis()
    plt.savefig(output_file, bbox_inches="tight")
    plt.tight_layout()
    plt.close()
    print(f"Saved as: {output_file}")


def getAllCountries():
    session = getSession()
    countries = []
    try:
        countries = session.query(CountryModel).order_by(CountryModel.name.asc()).all()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
        return countries


def getAllYearsByCountry(country):
    session = getSession()
    years = []
    try:
        session.add(country)
        for cyc in country.years.goup_by(CountryYearCriteriaModel.year_id):
            years.append(cyc.year)
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
        return years


def getAllCriteriaByYearCountry(country, year):
    session = getSession()
    criteria = []
    try:
        session.add(country)
        for cyc in country.years.filter(CountryYearCriteriaModel.year_id == year.id).all():
            criteria.append(cyc.criteria)
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
        return criteria


def getNumberOfEntries():
    count = 0
    session = getSession()
    try:
        count = session.query(func.count()).select_from(FindingRecommendationModel).scalar()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
        return count


def getCountryYearCriteriaWiseFindingRecommendation(ne):
    session = getSession()
    countries = dict()
    try:
        with tqdm(total=ne, desc="Plucking From Database") as pbar:
            for country in session.query(CountryModel).order_by(CountryModel.name.asc()).all():
                years = dict()
                for cyc in session.query(CountryYearCriteriaModel).join(YearModel).filter(
                    CountryYearCriteriaModel.country_id == country.id
                ).order_by(YearModel.name.asc(), CountryYearCriteriaModel.criteria_id.asc()).all():
                    if cyc.year_id not in years:
                        years[cyc.year_id] = {
                            "id": cyc.year.id,
                            "name": cyc.year.name,
                            "criteria": dict()
                        }

                    if cyc.criteria_id not in years[cyc.year_id]['criteria']:
                        years[cyc.year_id]['criteria'][cyc.criteria_id] = {
                            "id": cyc.criteria.id,
                            "title": cyc.criteria.title,
                            "findings_recommendations": dict()
                        }

                    findings_recommendations = dict()

                    for finding_recommendation in session.query(FindingRecommendationModel).filter(
                            FindingRecommendationModel.cyc_id == cyc.id).order_by(
                            FindingRecommendationModel.id.asc()).all():
                        findings_recommendations[finding_recommendation.id] = {
                            "id": finding_recommendation.id,
                            "finding": finding_recommendation.finding,
                            "recommendation": finding_recommendation.recommendation
                        }
                        pbar.update(1)
                    years[cyc.year_id]['criteria'][cyc.criteria_id]['findings_recommendations'] = findings_recommendations

                countries[country.id] = {
                    "id": country.id,
                    "name": country.name,
                    "years": years
                }
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
        return countries
