# Parse the Germanic Thesaurus into a machine-readable JSON format

"""
Regex

Fail:
\[D\d\|(?'definition'.+?)\]\s(?'alternatives'.+?)(?= [\s?\[])


"""

import csv
import json
import re

# test_string = "[D1|on all sides or in every direction] about, all over, everywhere, abroad, afloat, hereabout, hereabouts [D2|toward the opposite direction] about, back, backward, backwards, behind, down, downward, athwart, everywhere, here and there, to and fro"
# multiple_definitions_re = r"\[D\d\|(?'definition'.*?)\]\s(?'alternatives'.*?)(?=[$\[])"

# matches = re.finditer(multiple_definitions_re, test_string)

# for match in matches:
#     for group in range(0, len(match.groups())):
#         print(f"Group: '{group}'")

# input("Close now")

"""
english_to_germanic = {
    "just": {
        "Adverb": {
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
        }
    }
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
            
            pass
        
        line_count += 1
