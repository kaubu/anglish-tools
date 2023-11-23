# Parse the Germanic Thesaurus into a machine-readable JSON format

"""
Regex

Fail:
\[D\d\|(?'definition'.+?)\]\s(?'alternatives'.+?)(?= [\s?\[])


"""

import csv
import json
import re

test_string = "[D1|on all sides or in every direction] about, all over, everywhere, abroad, afloat, hereabout, hereabouts [D2|toward the opposite direction] about, back, backward, backwards, behind, down, downward, athwart, everywhere, here and there, to and fro"
multiple_definitions_re = r"\[D\d\|(?P<definition>.*?)\]\s(?P<alternatives>.*?)(?=[$\[])"

matches = re.finditer(multiple_definitions_re, test_string)

for match in matches:
    for group in range(1, len(match.groups())):
        print(f"Definition: {match.group('definition')}")
        print(f"Alternatives: {match.group('alternatives')}")
        print()

input("Close now")

"""
english_to_germanic = {
    "just": {
        "Adverb": {
            "alternatives": {
                "by a very small margin": [
                    "slightly",
                    "narrowly",
                    "barely",
                    "hardly",
                    "somewhat",
                    "tad",
                ],
                "for nothing other than": [
                    "alone",
                    "only",
                    "mainly",
                    "mostly",
                ],
                "not long ago": [
                    "freshly",
                    "late",
                    "lately",
                    "new",
                    "newly",
                    "now",
                    "only",
                ],
                "nothing more than": [
                    "only",
                    "but",
                    "nothing more than",
                ],
            },
            "germanic_like_alternatives": "merely",
            "details": {
                "notes": [],
                "examples": [
                    {
                        "example": "Just so you know/understand, ...",
                        "related_lemmas": "remember D2",
                    }
                ],
                "germanic_like_examples": [],
                "related_lemmas": []
            }
        }
    },
}

===

english_to_germanic = {
    LEMMA: {
        POS: {
            "alternatives": {
                DEFINITION1: [ALTERNATIVE1, ALTERNATIVE2],
            },
            "germanic_like_alternatives": GL_ALTERNATIVES_STRING,
            "details": {
                "notes": [NOTES],
                "examples": [
                    {
                        "example": EXAMPLE_GX,
                        "related_lemmas": RELATED_LEMMAS_OPTIONAL,
                    }
                ],
                "germanic_like_examples": [],
                "links": [LINKS_LX]
                "related_lemmas": [],
            }
        }
    },
}
"""

english_to_germanic = {}

with open("in/germanic_thesaurus.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            line_count += 1
            continue

        rank = row[0]
        lemmas = row[1]
        pos = row[2]
        germanic = row[3]
        germanic_like = row[4]
        details = row[5]

        lemmas = lemmas.split(",")
        lemmas = [l.strip() for l in lemmas]
        lemmas = [l.removeprefix("`") for l in lemmas]

        # Lemmas: ['time period']
        # Lemmas: ['title']
        # Lemmas: ['to all appearances', 'by all appearances', 'from all appearances']
        # print(f"Lemmas: {lemmas}")

        for lemma in lemmas:
            # If the word already exists
            if lemma in english_to_germanic:
                # If the parts of speech exists
                if pos in english_to_germanic[lemma]:
                    print(f"Something has gone wrong, POS already at {lemma}")
                else:
                    english_to_germanic[lemma][pos] = {
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
                    }
            pass
        
        line_count += 1
