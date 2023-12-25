"""
etymologies = {
    "Dodecanese": {
        "origin": "Greek",
        "sub_origins": ["Greek"],
    },
    "freckle": {
        "origin": "Norse",
        "sub_origins": ["Norse"],
    },
    "force": {
        "origin": "Mixed",
        "sub_origins": ["French", "Latin", "Norse"],
    }
}
"""

import json

WORD_LISTS = [
    ("./etymologies/words/french.txt", "French"),
    ("./etymologies/words/latin.txt", "Latin"),
    ("./etymologies/words/norse.txt", "Norse"),
    ("./etymologies/words/greek.txt", "Greek"),
    ("./etymologies/words/unknown.txt", "Unknown"),
    ("./etymologies/words/old_english.txt", "Old English"),
]

etymologies = {}

for word_list_pairs in WORD_LISTS:
    word_list = word_list_pairs[0]
    current_lang = word_list_pairs[1]

    with open(word_list, "r") as f:
        for line in f:
            line = line.strip()

            # If the word exists
            if line in etymologies:
                origin = etymologies[line].get("origin")
                sub_origins = etymologies[line].get("sub_origins")

                # If it is not already mixed
                if origin != "Mixed":
                    etymologies[line]["origin"] = "Mixed"
                
                # If new source is not already in sub_origins, add it
                if current_lang not in sub_origins:
                    etymologies[line]["sub_origins"].append(current_lang)
            # If the word doesn't exist
            else:
                etymologies[line] = {
                    "origin": current_lang,
                    "sub_origins": [current_lang]
                }

with open("./out/etymologies.json", "w") as f:
    json.dump(etymologies, f)
