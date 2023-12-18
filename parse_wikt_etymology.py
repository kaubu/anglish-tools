import json

# Download here: https://kaikki.org/dictionary/rawdata.html
WIKTEXTRACT_PATH = "/run/media/user/Expansion/Documents/Coding/DATA/raw-wiktextract-data-2023-12-01.json"

# https://kaikki.org/dictionary/English/index.html
ENGLISH_PATH = "/run/media/user/Expansion/Documents/Coding/DATA/kaikki.org-dictionary-English.json"
"""
{
  "forms": [
    {
      "form": "aard-varks",
      "tags": [
        "plural"
      ]
    }
  ],
  "head_templates": [
    {
      "args": {},
      "expansion": "aard-vark (plural aard-varks)",
      "name": "en-noun"
    }
  ],
  "lang": "English",
  "lang_code": "en",
  "pos": "noun",
  "senses": [
    {
      "alt_of": [
        {
          "word": "aardvark"
        }
      ],
      "categories": [
        "English archaic forms",
        "English countable nouns",
        "English lemmas",
        "English multiword terms",
        "English nouns"
      ],
      "glosses": [
        "Archaic spelling of aardvark."
      ],
      "links": [
        [
          "aardvark",
          "aardvark#English"
        ]
      ],
      "tags": [
        "alt-of",
        "archaic"
      ]
    }
  ],
  "word": "aard-vark"
}
"""

"""
etymologies = {
    WORD: SENSES = [
        {
            glosses: GLOSSES_STRING,
            etymologies: [
                "From Old Norse"
                "Derived from Old English"
                etc
            ]   
        }
    ]
}
"""

categories_replace = {
    "English terms derived from Old English": "Derived from Old English",
    "English terms inherited from Old English": "Inherited from Old English",

    "English terms inherited from Proto-Germanic": "Inherited from Proto-Germanic",
    "English terms inherited from Proto-West Germanic": "Inherited from Proto-West Germanic",

    "English terms derived from North Germanic languages": "Derived from a North Germanic language",

    "English terms derived from Old Norse": "Derived from Old Norse",
    "English terms borrowed from Old Norse": "Borrowed from Old Norse",

    "English terms derived from Latin": "Derived from Latin",
    "English terms borrowed from Latin": "Borrowed from Latin",
    "English learned borrowings from Latin": "Learned Borrowing from Latin",
    "English pseudo-loans from Latin": "Pseudo-loan from Latin",    # This fucking…
    "English terms calqued from Latin": "Calqued from Latin",
    "English unadapted borrowings from Latin": "Unadapted Borrowing from Latin",

    "English terms borrowed from Ancient Greek": "Borrowed from Ancient Greek",
    "English learned borrowings from Ancient Greek": "Learned Borrowing from Ancient Greek",
    "English terms calqued from Ancient Greek": "Calque from Ancient Greek",

    "English terms derived from Norman": "Derived from Norman",

    "English terms derived from Old French": "Derived from Old French",
    "English terms derived from Middle French": "Derived from Middle French",
    "English terms borrowed from Middle French": "Borrowed from Middle French",
    "English terms derived from French": "Derived from French",
    "English terms borrowed from French": "Borrowed from French",
    "English terms calqued from French": "Calqued from French",
}

etymologies = {}
DEBUG = True
MODE = "Full"   # Full | English

def get_etymologies(cs: list) -> list:
    es = []
    
    if MODE == "Full":
        for c in cs:
            if c["name"].strip() in categories_replace:
                es.append(categories_replace[c["name"].strip()])
    elif MODE == "English":
        for c in cs:
            """
            c = {
            "kind": "other",
            "name": "English entries with topic categories using raw markup",
            "parents": [
                "Entries with topic categories using raw markup",
                "Entry maintenance"
            ],
            "source": "w"
            },
            """

            if c["name"].strip() in categories_replace:
                # to_replace = categories[categories.index(c)]
                # print(f"categories_replace[c[name] = {categories_replace[c['name']]}")
                es.append(categories_replace[c["name"].strip()])

    return es

with open(WIKTEXTRACT_PATH, "r", encoding="utf-8") as f:
    word_count = 0

    for line in f:
        word_count += 1
        # 9114889 (all words)
        # 1261507 (English)
        # print(f"Loading line {word_count} / 1261507 ({(word_count / 1261507) * 100:.2f}%)")
        data = json.loads(line)

        if DEBUG:
            print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
            input("Continue?")
            print("===\n\n\n===")
        
        # lang = data.get("lang")
        # lang_code = data.get("lang_code")

        # if lang != "English" or lang_code != "en":
        #     continue
        
        word = data.get("word")
        senses = data.get("senses")

        if not senses:
            continue

        if MODE == "Full":
            glosses = senses.get("glosses")
            categories = senses.get("categories")

            if glosses == None:
                continue
            elif categories == None:
                continue

            e = get_etymologies(categories)

            if not e or len(e) <= 0:
                continue
            # else:
                # print(f"word = {word}; e = {e}")

            if not word in etymologies:
                etymologies[word] = []

            for gloss in glosses:
                new_entry = {
                    "gloss": gloss,
                    "etymologies": e,
                }

                # print(f"new_entry = {new_entry}")

                etymologies[word].append(new_entry)
        elif MODE == "English":
            for sense in senses:
                glosses = sense.get("glosses")
                categories = sense.get("categories")

                if glosses == None:
                    continue
                elif categories == None:
                    continue

                e = get_etymologies(categories)

                if not e or len(e) <= 0:
                    continue
                # else:
                    # print(f"word = {word}; e = {e}")

                if not word in etymologies:
                    etymologies[word] = []

                for gloss in glosses:
                    new_entry = {
                        "gloss": gloss,
                        "etymologies": e,
                    }

                    # print(f"new_entry = {new_entry}")

                    etymologies[word].append(new_entry)

with open("out/etymologies.json", "w") as f:
    json.dump(etymologies, f)
