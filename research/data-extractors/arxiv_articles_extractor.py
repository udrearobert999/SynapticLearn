import arxiv
import pandas as pd
from sklearn.model_selection import train_test_split

# Define your categories list
CATEGORIES = [
    "cond-mat.quant-gas",  # Quantum Gases
    "quant-ph",  # Quantum Information
    "hep-th",  # High Energy Physics - Theory
    "hep-ph",  # High Energy Physics - Phenomenology
    "hep-lat",  # High Energy Physics - Lattice
    "hep-ex",  # High Energy Physics - Experiment
    "cond-mat.str-el",  # Strongly Correlated Electrons
    "cond-mat.supr-con",  # Superconductivity
    "cond-mat.mes-hall",  # Mesoscale and Nanoscale Physics
    "math.QA",  # Quantum Algebra
]

PAPERS_LIMIT = 2

client = arxiv.Client()

# List to hold DataFrames for all categories
dfs = []

# Iterate over each category and fetch papers
for category in CATEGORIES:
    # Define your search with a specific category
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=PAPERS_LIMIT,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    # Fetch the results and store them in a list
    papers = []
    for result in client.results(search):
        papers.append(
            {
                "Category": category,
                "Title": result.title,
                "Authors": ", ".join(author.name for author in result.authors),
                "Abstract": result.summary,
                "URL": result.entry_id,
            }
        )

    # Convert the list of papers to a pandas DataFrame and add it to the dfs list
    dfs.append(pd.DataFrame(papers))

# Concatenate all DataFrames in the dfs list into one DataFrame
all_papers_df = pd.concat(dfs, ignore_index=True)
train_df, test_df = train_test_split(
    all_papers_df, test_size=0.25, random_state=42
)  # 25% for testing

# Save the datasets into CSV files
train_df.to_csv("./data/train_data.csv", index=False)
test_df.to_csv("./data/test_data.csv", index=False)
