# Policy-Analytics

Policy-Analytics is an advanced data analysis project focused on extracting, processing, and analyzing policy-related data using state-of-the-art Natural Language Processing (NLP) techniques and Machine Learning models. This repository showcases an innovative approach to uncovering trends and insights from policy recommendations across various regions, countries, and time frames. Through sentiment analysis, text mining, and data visualization, Policy-Analytics enables deep insights into global policy frameworks.

### Key Features:
- **NLP and ML Models** for sentiment analysis, text classification, and keyword extraction.
- **Time Series Analysis** of policy topics across multiple regions and years.
- **Word Cloud Generation** to visualize the most relevant policy keywords.
- **Category Analysis** of recommendations by economic, environmental, social, and gender-related policies.

## Technologies Used:
- **Python** (Data Processing, NLP, ML)
- **Pandas**, **NumPy**, **Matplotlib** (Data Manipulation and Visualization)
- **Natural Language Toolkit (NLTK)** (Text Processing and Sentiment Analysis)
- **spaCy** (Text Mining)
- **WordCloud** (Term Frequency Visualization)
- **TQDM** (Progress Tracking for Large Datasets)

---

## Project Structure:

- **`generate_keywords.py`**: Extracts keywords from policy documents and saves them for analysis.
- **`generate_wordclouds.py`**: Generates word clouds from the extracted keywords, providing a visual representation of frequently mentioned terms.
- **`generate_climate_ts.py`**: Analyzes and visualizes trends in climate-related policy recommendations over time.
- **`generate_gender_ts.py`**: Analyzes and visualizes trends in gender-related policy recommendations over time.
- **`generate_categories_graph.py`**: Generates visual charts to showcase the distribution of policy recommendations by category (e.g., economic reforms, environmental policies, gender-related policies).
- **`helper.py`**: Contains core functions used across the project, such as NLP processing, data filtering, and chart generation.

---

## How to Get Started

### Step 1: Set Up the Environment

You'll need to set up a Python virtual environment to manage project dependencies. Follow these steps to create and activate the environment on macOS or Linux:

1. Open your terminal and navigate to your project directory:
    ```bash
    cd /path/to/your/project
    ```
2. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
3. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

### Step 2: Install Project Dependencies

1. Once the virtual environment is activated, install the required dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
2. Verify the installation:
    ```bash
    pip list
    ```

---

## Running the Project

### 1. **Generating Keywords**

To generate keywords from policy documents:
```bash
python generate_keywords.py
```
This step processes the `oecd_findings_recommendations.pkl` file and saves the generated keywords in `oecd_keywords_df.pkl` for future use.

---

### 2. **Generating Word Clouds**

To create visual representations of keyword frequency, run:
```bash
python generate_wordclouds.py
```
This will generate word clouds and save them in the `output/word_clouds/` directory. You can modify the output path and configurations directly in `generate_wordclouds.py`. Here's a simple example to generate a word cloud:

```python
create_word_cloud(
    df=df_collection,
    start_year=2000,
    end_year=2010,
    column="recommendations",
    color="blue",
    title="Recommendations Word Cloud (2000-2010)",
    output_dir=output_dir
)
```

**Customization Options:**
- `column`: Can be set to "findings", "recommendations", or "all".
- `color`: Defines the color of the word cloud (options: "blue", "orange").
- `countries`: You can specify countries or regions to filter the data (e.g., `countries="America"` or `countries=["Japan", "Australia"]`).

---

### 3. **Generating Time Series Graphs**

To analyze trends over time:
- **Climate-related graph**:
    ```bash
    python generate_climate_ts.py
    ```
- **Gender-related graph**:
    ```bash
    python generate_gender_ts.py
    ```

The time series graphs will be saved in the `output/time_series/` directory. Here's an example usage of `generate_ts` to create a graph:

```python
generate_ts(
    df=df_collection,
    related_terms=gender_related_terms,
    start_year=2000,
    end_year=2023,
    relevancy="gender",
    color="#4392CC",
    title="Gender-Related Terms Occurrences Over Time (2000-2023)",
    output_dir=output_dir
)
```

You can also generate time series graphs for specific countries or regions using the `countries` parameter.

---

### 4. **Generating Recommendations Category Charts**

To analyze and visualize the distribution of recommendations across categories, run:
```bash
python generate_categories_graph.py
```
This will generate bar charts that break down recommendations by categories such as "economic reforms", "environmental policies", and "social policies".

---

## Example Visualizations

### Word Clouds
- Word clouds for terms like "recommendations" or "findings" highlight the most commonly mentioned terms in policy documents, filtered by region or year.

### Time Series Graphs
- Time series graphs show the trends in policy focus areas such as climate or gender, illustrating how these issues have gained or lost attention over time.

### Category Charts
- These charts provide a breakdown of recommendations across different categories (e.g., economic vs. environmental policies).

---

## Customization Options

You can further customize the analysis by:
- Modifying keyword lists in `terms.py` to focus on different policy areas.
- Adjusting year ranges or filtering specific countries/regions in the provided scripts.
- Changing the appearance of charts and visualizations using parameters in the helper functions (e.g., colors, sizes, output directories).

---

## Conclusion

This repository demonstrates a powerful and versatile toolset for analyzing large-scale policy data. By using Policy-Analytics, researchers and data scientists can quickly identify trends, generate insights, and create professional visualizations to aid decision-making in public policy.

Whether you are exploring gender equality in different regions, tracking the evolution of climate policy, or identifying emerging economic trends, Policy-Analytics provides the foundation for deep and meaningful analysis.
