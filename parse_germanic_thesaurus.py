# Parse the Germanic Thesaurus into a machine-readable JSON format

import csv
import json

"""
array around entry

english_to_germanic[lemma][pos] = [{
    "alternatives": {
        DEFINITION1: [ALTERNATIVE1, ALTERNATIVE2],
    },
    "germanic_like_alternatives": germanic_like,
    "details": {
        "notes": [NOTES],
        "examples": [
            {
                "example": EXAMPLE_GX,
                "related_lemmas": RELATED_LEMMAS_OPTIONAL,
            }
        ],
        "germanic_like_examples": [],
        "links": [LINKS_LX],
        "related_lemmas": [],
    }
}]
"""

def process_pos(pos: str) -> str:
    pos = pos.strip()
    
    if pos == "n": return "Noun"

    pos = pos.replace("adj", "Adjective")
    pos = pos.replace("adv", "Adverb")
    pos = pos.replace("conj", "Conjunction")
    pos = pos.replace("interj", "Interjection")
    pos = pos.replace("phr", "Phrase")
    pos = pos.replace("pref", "Prefix")
    pos = pos.replace("prep phr", "Prepositional Phrase")
    pos = pos.replace("prep", "Preposition")
    pos = pos.replace("suff", "Suffix")
    pos = pos.replace("vb", "Verb")

    return pos

def process_germanic(g: str) -> str:
    germanic = g.replace(" [D", "<br/><br/>[D")
    germanic = germanic.replace("[D", "[Definition ")
    germanic = germanic.replace("|D", "|Definition ")
    return germanic

def process_details(d: str) -> str:
    details = d.replace("\n", "<br/>")
    details = details.replace("[N", "[Note ")
    details = details.replace("|N", "|Note ")
    details = details.replace("[G", "[Example ")
    details = details.replace("|G", "|Example ")
    details = details.replace("[F", "[Germanic-like example ")
    details = details.replace("|F", "|Germanic-like example ")
    details = details.replace("[L", "[Link ")
    details = details.replace("|L", "|Link ")
    details = details.replace("[S", "[Related lemmas")
    details = details.replace("|S", "|Related lemmas")
    details = details.replace("[D", "[Definition ")
    details = details.replace("|D", "|Definition ")

    return details

english_to_germanic = {}

germanic_thesaurus = {}
with open("in/germanic_thesaurus_2.csv", "r") as f:
    germanic_thesaurus = list(csv.reader(f))

with open("in/germanic_thesaurus_2.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            line_count += 1
            continue

        rank = row[0]
        lemmas = row[1]
        pos = process_pos(row[2])
        germanic = row[3]
        germanic = process_germanic(germanic)
        germanic_like = row[4]
        details = row[5]
        details = process_details(details)
        
        # Add O(NUMBER)

        lemmas = lemmas.split(",")
        lemmas = [l.strip() for l in lemmas]
        lemmas = [l.removeprefix("`") for l in lemmas]

        # Lemmas: ['time period']
        # Lemmas: ['title']
        # Lemmas: ['to all appearances', 'by all appearances', 'from all appearances']
        # print(f"Lemmas: {lemmas}")

        # if "." in rank:
        #     in_sub_lemma = True
        #     sub_lemmas_since_root = int(rank.split(".")[1])
        #     # sub_lemma_root = ['606', '`term', 'n', '', '', '[S] come to terms with, in terms of', '']
        #     sub_lemma_root = germanic_thesaurus[line_count - sub_lemmas_since_root]
        #     print(f"sub_lemma_root = {sub_lemma_root}")
        #     input("Continue?\n")
        # elif "." not in rank:
        #     in_sub_lemma = False
        #     sub_lemma_root = None

        sub_lemmas = []

        # print(f"germanic_thesaurus[line_count + 1] = {germanic_thesaurus[line_count + 1]}")
        # germanic_thesaurus[line_count + 1] = ['51.1', '`just as', 'phr', '',
        # '', "[G1] He left just as I was coming in → He left right as/when I
        # was coming in → He left at the same time as I was coming in\n[G2]
        # Just as you'd ... → (Much) In (much) the same way you'd ... → As you
        # would ...\n[S] equally", '']

        # If you are on the root lemma
        if not line_count + 1 == len(germanic_thesaurus):
            if ".1" in germanic_thesaurus[line_count + 1][0]:
                # print(f"find: .1 in {germanic_thesaurus[line_count + 1]}")
                sl_count = 0
                while True:
                    if "." in germanic_thesaurus[line_count + 1 + sl_count][0]:
                        # print(f"find: . in {germanic_thesaurus[line_count + 1 + sl_count]}")
                        sl = germanic_thesaurus[line_count + 1 + sl_count]
                        sl[2] = process_pos(sl[2])
                        sl[3] = process_germanic(sl[3])
                        sl[5] = process_details(sl[5])

                        sub_lemmas.append(sl)
                    else:
                        break

                    sl_count += 1
        
        # if len(sub_lemmas) > 1:
        #     print(f"\n\n=====\nSub lemmas: {sub_lemmas}")
        #     input("Continue?")

        for i, lemma in enumerate(lemmas):
            # If the word already exists
            if lemma in english_to_germanic:
                # If the parts of speech exists
                if pos in english_to_germanic[lemma]:
                    # print(f"Something has gone wrong, POS already at {lemma}")

                    english_to_germanic[lemma][pos].append({
                        "alternatives": germanic,
                        "germanic_like_alternatives": germanic_like,
                        "details": details,
                        "sub_lemmas": sub_lemmas,
                    })

                    
                else:
                    english_to_germanic[lemma][pos] = [{
                        "alternatives": germanic,
                        "germanic_like_alternatives": germanic_like,
                        "details": details,
                        "sub_lemmas": sub_lemmas,
                    }]
            # If the word doesn't exist
            else:
                english_to_germanic[lemma] = {
                    pos: [{
                        "alternatives": germanic,
                        "germanic_like_alternatives": germanic_like,
                        "details": details,
                        "sub_lemmas": sub_lemmas,
                    }]
                }
        
        line_count += 1

with open("out/english_to_germanic.json", "w") as f:
    json.dump(english_to_germanic, f)
