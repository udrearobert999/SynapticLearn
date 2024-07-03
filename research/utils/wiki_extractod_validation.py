import requests

from utils import categories

API_ENDPOINT = "https://en.wikipedia.org/w/api.php"


def get_category_members(category, cmtype="page|subcat", limit=10, continue_from=None):
    """
    Modified to check if any members exist in the category.
    """
    try:
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": "Category:" + category,
            "cmtype": cmtype,
            "cmlimit": limit,
        }
        if continue_from:
            params["cmcontinue"] = continue_from

        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()

        pages = data["query"]["categorymembers"]
        exists = len(pages) > 0
        continue_from = data.get("continue", {}).get("cmcontinue")

        return exists, pages, continue_from
    except Exception as e:
        print(f"Error fetching category members for {category}: {e}")
        return False, [], None


def category_exists(category):
    """
    Check if a given category exists in Wikipedia.
    """
    exists, _, _ = get_category_members(category, limit=1)
    return exists


topics = [
    "Arthrology",
    "Auxology",
    "Axiology",
    "Carcinology",
    "Chronobiology",
    "Conchology",
    "Cosmology",
    "Dialectology",
    "Epistemology",
    "Ethnobiology",
    "Ethnology",
    "Eugenics",
    "Floristry",
    "Geomicrobiology",
    "Gerontology",
    "Hepatology",
    "Herpetology",
    "Histology",
    "Horology",
    "Hydrostatics",
    "Laryngology",
    "Lexicology",
    "Lichenology",
    "Mycology",
    "Myrmecology",
    "Nephrology",
    "Oology",
    "Otology",
    "Paleozoology",
    "Palynology",
    "Papyrology",
    "Phenomenology",
    "Phycology",
    "Pomology",
    "Prosthetics",
    "Soteriology",
    "Taphonomy",
    "Taxidermy",
    "Thanatology",
]
existing_categories = [category for category in topics if category_exists(category)]

filtered_list = []
for category in existing_categories:
    if category not in categories:
        filtered_list.append(category)

import numpy as np

print(np.unique(filtered_list).tolist())
