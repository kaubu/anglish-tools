# ᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫
# Python 3.9 or later

"""
Word: dere
Ang Spelling: 
Meaning: ᛫ hurt ᛫ harm ᛫ injury ᛬ to hurt ᛫ to harm ᛫ to injure ᛫
Kind: N᛬V
Forebear: dēre
Taken from: ME
Notes: 


Definitions: {'N': ['hurt', 'harm', 'injury'], 'V': ['to hurt', 'to harm', 'to injure']}
"""

import csv
import json

POS_DIVIDER = "᛬"

def split_definitions(definitions: str, pos: str):
    definitions = definitions.strip()
    definitions = definitions.removeprefix("᛫ ")
    definitions = definitions.removesuffix(" ᛫")

    if POS_DIVIDER in definitions:
        # There are multiple parts of speech, loop for each one
        pos_dict = {}

        poses = pos.strip().split(POS_DIVIDER)
        pos_definitions = definitions.split(POS_DIVIDER)
        # print(pos_definitions)

        for i, p in enumerate(poses):
            # original_definitions = pos_definitions[i]
            # N, V, AJ
            pos_definitions[i] = pos_definitions[i].split("᛫")
            pos_definitions[i] = [d.strip() for d in pos_definitions[i]]

            pos_dict[p] = pos_definitions[i]
        
        return pos_dict
    else:
        # There is only one parts of speech
        definitions = definitions.split("᛫")
        definitions = [d.strip() for d in definitions]
        # if definitions[0] == "": definitions.pop(0)

        return {pos: definitions}

# split_definitions_examples = [
#     ["᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫", "AJ"],
#     [" 	᛫ a region in Poland ᛫", "N(P)"],
#     [" 	᛫ guidance ᛫ instruction ᛫", "N"],
#     ["᛫ weak ᛫ watery ᛫ feeble wavering ᛫", "AJ"],
#     ["᛫ a manner ᛫ a fashion ᛫ a method ᛬ to make apparent ᛬ sagacious ᛫ prudent ᛫", "N᛬V᛬AJ"]
# ]

# for s in split_definitions_examples:
#     a = split_definitions(s[0], s[1])
#     print(a)

# Form:
# "english definition lemma": {
#   "anglish_word": X,
#   "anglish_spelling": X,
#   ""
# }

"""
Form:
{
    "sequel": {
        "noun": [
            {
                "definitions": "a sequel, the film after another film",
                "anglish_word": "aftercoming",
                "anglish_spelling": "aftercumming",
                "forebear": "~",
                "taken_from": "NE",
                "notes": "",
            }
        ]
    }
}
"""
english_to_anglish = {}

with open("the_anglish_wordbook.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")
    line_count = 0
    
    for row in csv_reader:
        # row = word.split(",", 7);

        word = row[0]
        anglish_spelling = row[1]
        meaning = row[2]   # No use after definitions
        kind = row[3]      # No use after definitions
        forebear = row[4]
        taken_from = row[5]
        notes = row[6]

        all_definitions = split_definitions(meaning, kind)

        # print(all_definitions)
        # all_definitions = {'N': ['time long past'], 'AV': ['in the past']}

        # print(definitions)

#         print(f"===\nWord: {word}\n\
# Ang Spelling: {anglish_spelling}\n\
# Meaning: {meaning}\n\
# Kind: {kind}\n\
# Forebear: {forebear}\n\
# Taken from: {taken_from}\n\
# Notes: {notes}\n\
# \n\
# Definitions: {definitions}")

        # print(all_definitions)

        for kind, definitions in all_definitions.items():
            
            kind.replace("AC", "Acronym")
            kind.replace("AD", "Adverb")
            kind.replace("ADJ", "Adjective")
            kind.replace("ADV", "Adverb")
            kind.replace("AJ", "Adjective")
            kind.replace("AJ(P)", "Proper Adjective")
            kind.replace("AV", "Adverb")
            kind.replace("C", "Conjunction")
            kind.replace("D", "Determiner")
            kind.replace("I", "Interjection")
            kind.replace("N", "Noun")
            kind.replace("N(P)", "Proper Noun")
            kind.replace("N(PRO)", "Pronoun")
            kind.replace("N(PN)", "Pronoun")
            kind.replace("P", "Preposition")
            kind.replace("PN", "Proper Noun")
            kind.replace("PP", "Prepositional Phrase")
            kind.replace("PHRASE", "Phrase")
            kind.replace("PREFIX", "Prefix")
            kind.replace("SUFFIX", "Suffix")
            kind.replace("V", "Verb")
            
            for definition in definitions:
                # If there is already an English word in the set
                if definition in english_to_anglish:
                    # If there is already a POS of that definition
                    if kind in english_to_anglish[definition]:
                        english_to_anglish[definition][kind].append({
                            "anglish_word": word,
                            "anglish_spelling": anglish_spelling,
                            "forebear": forebear,
                            "taken_from": taken_from,
                            "notes": notes,
                        })
                    # If the word exists but doesn't have the same kind/POS
                    else:
                        english_to_anglish[definition].update({kind: [
                            {
                                "anglish_word": word,
                                "anglish_spelling": anglish_spelling,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            }
                        ]})
                # If the word doesn't exist already
                else:
                    english_to_anglish.update({definition: {
                        kind: [
                            {
                                "anglish_word": word,
                                "anglish_spelling": anglish_spelling,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            }
                        ]
                    }})
    
        line_count += 1

with open("english_to_anglish.json", "w") as f:
    # f.write(english_to_anglish)
    json.dump(english_to_anglish, f)