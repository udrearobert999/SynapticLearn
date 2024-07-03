import requests
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from sklearn.model_selection import train_test_split

from config import CATEGORIES, SEED

API_ENDPOINT = "https://en.wikipedia.org/w/api.php"


def prepare_data(train_data, eval_data, test_data):
    pass


def clean_wikipedia_content(article_content):
    """
    Cleans the provided Wikipedia article content by removing specified sections,
    all occurrences of '==...==', unnecessary spaces and newlines, while preserving LaTeX expressions.

    :param article_content: A string containing the content of a Wikipedia article.
    :return: Cleaned article content as a string.
    """
    # Remove specified sections
    sections_to_remove = (
        r"(== References ==.*?)(?=(== .+? ==|$))|"
        r"(== External links ==.*?)(?=(== .+? ==|$))|"
        r"(== Gallery ==.*?)(?=(== .+? ==|$))|"
        r"(== Footnotes ==.*?)(?=(== .+? ==|$))"
    )
    article_content = re.sub(sections_to_remove, "", article_content, flags=re.DOTALL)

    # Remove '==...==' occurrences everywhere
    section_headers_pattern = r"==[^=]*=="
    article_content = re.sub(section_headers_pattern, "", article_content)

    # Handle LaTeX expressions separately to avoid truncation
    parts = re.split(r"(\{\s*\\displaystyle[^\}]*\})", article_content)
    cleaned_parts = []
    for part in parts:
        if not re.match(r"\{\s*\\displaystyle[^\}]*\}", part):
            # Remove unnecessary spaces and newlines
            part = re.sub(r"(\s{2,}|\n{2,})", " ", part)
        cleaned_parts.append(part)
    cleaned_content = "".join(cleaned_parts)

    return cleaned_content


def get_page_content(pageid):
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "inprop": "url",
            "pageids": pageid,
            "explaintext": True,
        }
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()
        page = data["query"]["pages"][str(pageid)]
        if "extract" in page and "fullurl" in page:
            title = page.get("title", "No Title")  # Fetch the title
            return title, page["extract"], page["fullurl"]
        else:
            return None, None, None
    except Exception as e:
        print(f"Error fetching page content for page ID {pageid}: {e}")
        return None, None, None


def get_category_members(category, limit=1000, continue_from=None):
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:" + category,
        "cmtype": "page",
        "cmlimit": limit,
        "cmcontinue": continue_from or "",
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()

    pages = data["query"]["categorymembers"]
    continue_from = data.get("continue", {}).get("cmcontinue")
    return pages, continue_from


def fetch_category_articles(category, max_articles):
    articles_info = []
    continue_from = None
    with ThreadPoolExecutor(max_workers=4) as executor:
        while len(articles_info) < max_articles:
            pages, continue_from = get_category_members(
                category, continue_from=continue_from
            )
            future_to_page = {
                executor.submit(get_page_content, page["pageid"]): page
                for page in pages
            }
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    title, content, url = future.result()

                    cleaned_content = clean_wikipedia_content(content)

                    # Check if the cleaned content has at least 200 words
                    if cleaned_content and url and len(cleaned_content.split()) >= 250:
                        articles_info.append(
                            {
                                "title": title,  # Include the title
                                "label": category,
                                "text": cleaned_content,
                                "url": url,
                            }
                        )

                except Exception as e:
                    print(f"Error fetching content for page {page['title']}: {e}")

            if len(articles_info) >= max_articles or not continue_from:
                break
    return articles_info[:max_articles]


def save_to_excel(data, path):
    df = pd.DataFrame(data)
    df.fillna("", inplace=True)
    df.to_excel(path, index=False)


def train_eval_test_split(data):
    # Split the data into training, validation, and test sets (80%, 10%, 10%)

    train_df, temp_df = train_test_split(
        data, test_size=0.2, stratify=data["Category"], random_state=SEED
    )
    eval_df, test_df = train_test_split(
        temp_df, test_size=0.5, stratify=temp_df["Category"], random_state=SEED
    )

    return train_df, eval_df, test_df


def discard_unseened_categories(train_df, eval_df, test_df):
    train_classes = set(train_df["Category"])
    val_classes = set(eval_df["Category"])
    test_classes = set(test_df["Category"])

    common_classes = train_classes & val_classes & test_classes
    train_df = train_df[train_df["Category"].isin(common_classes)]
    eval_df = eval_df[eval_df["Category"].isin(common_classes)]
    test_df = test_df[test_df["Category"].isin(common_classes)]

    return train_df, eval_df, test_df


def main():
    MAXIMUM_ARTICLES_PER_CATEGORY = 500
    all_articles = []

    for category in CATEGORIES:
        category_articles_info = fetch_category_articles(
            category, MAXIMUM_ARTICLES_PER_CATEGORY
        )

        all_articles.extend(category_articles_info)

    all_articles_df = pd.DataFrame(all_articles)

    class_counts = all_articles_df["Category"].value_counts()
    valid_classes = class_counts[class_counts >= 10].index
    filtered_df = all_articles_df[all_articles_df["Category"].isin(valid_classes)]

    train_df, eval_df, test_df = train_eval_test_split(filtered_df)
    train_df, eval_df, test_df = discard_unseened_categories(train_df, eval_df, test_df)

    # Save the datasets to Excel files
    save_to_excel(train_df, "../data/wiki_train.xlsx")
    save_to_excel(eval_df, "../data/wiki_eval.xlsx")
    save_to_excel(test_df, "../data/wiki_test.xlsx")


if __name__ == "__main__":
    main()
