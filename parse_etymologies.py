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
    ("./etymologies/words/german.txt", "German"),
    ("./etymologies/words/old_english.txt", "Old English"),
    ("./etymologies/words/germanic.txt", "Germanic"),
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

                is_germanic = False

                """
                "birth": {
                    "origin": "Mixed",
                    "sub_origins": ["Norse", "Germanic"]
                },
                """

                # If it is not already mixed
                if ("Old English" in sub_origins
                    or "German" in sub_origins
                    or "Germanic" in sub_origins
                    or "Norse" in sub_origins) and (not ("French" in sub_origins
                        or "Latin" in sub_origins
                        or "Greek" in sub_origins
                        or "Unknown" in sub_origins
                        ) and not (
                            current_lang == "Latin"
                            or current_lang == "Greek"
                            or current_lang == "Unknown"
                        )):
                    
                    if line == "birth":
                        print(f"set 'birth' to Germanic")
                        print(f"look before = {etymologies[line]}")

                    etymologies[line]["origin"] = "Germanic"

                    is_germanic = True

                elif origin != "Mixed" and not is_germanic:
                    if line == "birth": print(f"set 'birth' to Mixed")
                    etymologies[line]["origin"] = "Mixed"
                
                # Check for Germanic-ness
                if (
                    "Old English" in sub_origins
                    or "German" in sub_origins
                    or "Germanic" in sub_origins
                    or "Norse" in sub_origins
                ) and not (
                    "Latin" in sub_origins
                    or "French" in sub_origins
                    or "Greek" in sub_origins
                    or "Unknown" in sub_origins
                ):
                    is_germanic = True

                if ("Latin" in sub_origins
                    or "French" in sub_origins) and (not ("Old English" in sub_origins
                    or "German" in sub_origins
                    or "Germanic" in sub_origins
                    or "Norse" in sub_origins
                    or "Greek" in sub_origins
                    or "Unknown" in sub_origins) and not (
                        current_lang == "Old English"
                        or current_lang == "German"
                        or current_lang == "Germanic"
                        or current_lang == "Norse"
                        or current_lang == "Greek"
                        or current_lang == "Unknown"
                    )):
                    etymologies[line]["origin"] = "Romance"
                    if line == "birth": print(f"set 'birth' to Romance")
                elif origin != "Mixed" and not is_germanic:
                    if line == "birth":
                        print(f"set 'birth' to Mixed 2")
                        print(f"look before = {etymologies[line]}")
                    etymologies[line]["origin"] = "Mixed"
                
                # If new source is not already in sub_origins, add it
                if current_lang not in sub_origins:
                    etymologies[line]["sub_origins"].append(current_lang)
                
                if line == "birth": 
                        print(f"look after = {etymologies[line]}")
            # If the word doesn't exist
            else:
                etymologies[line] = {
                    "origin": current_lang,
                    "sub_origins": [current_lang]
                }

with open("./out/etymologies.json", "w") as f:
    json.dump(etymologies, f)
