# ᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫
# Python 3.9 or later

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
            original_definitions = pos_definitions[i]
            original_definitions = original_definitions.removeprefix("᛫ ")
            original_definitions = original_definitions.replace(" ᛫", ",")
            original_definitions = original_definitions.strip()

            # N, V, AJ
            pos_definitions[i] = pos_definitions[i].split("᛫")
            pos_definitions[i] = [d.strip() for d in pos_definitions[i]]

            pos_dict[p] = (pos_definitions[i], original_definitions)
        
        return pos_dict
    else:
        original_definitions = definitions
        original_definitions = original_definitions.removeprefix("᛫ ")
        original_definitions = original_definitions.replace(" ᛫", ",")
        original_definitions = original_definitions.strip()

        # There is only one parts of speech
        definitions = definitions.split("᛫")
        definitions = [d.strip() for d in definitions]
        # if definitions[0] == "": definitions.pop(0)

        return {pos: (definitions, original_definitions)}

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

        # Definitions:
        # (['per'], 'per')
        for kind, definitions in all_definitions.items():
            
            kind = kind.replace("PHRASE", "Phrase")
            kind = kind.replace("PREFIX", "Prefix")
            kind = kind.replace("SUFFIX", "Suffix")
            kind = kind.replace("AJ(P)", "Proper Adjective")
            kind = kind.replace("N(PRO)", "Pronoun")
            kind = kind.replace("N(PN)", "Pronoun")
            kind = kind.replace("N(P)", "Proper Noun")
            kind = kind.replace("PP", "Prepositional Phrase")
            kind = kind.replace("PN", "Proper Noun")
            kind = kind.replace("AC", "Acronym")
            kind = kind.replace("AD", "Adverb")
            kind = kind.replace("ADJ", "Adjective")
            kind = kind.replace("ADV", "Adverb")
            kind = kind.replace("AJ", "Adjective")
            kind = kind.replace("AV", "Adverb")
            kind = kind.replace("C", "Conjunction")
            kind = kind.replace("D", "Determiner")
            kind = kind.replace("I", "Interjection")
            kind = kind.replace("N", "Noun")
            kind = kind.replace("P", "Preposition")
            kind = kind.replace("V", "Verb")
            
            for definition in definitions[0]:
                # "to help" → "help"
                # "a soldier" → "soldier"
                if kind == "Verb":
                    definition = definition.removeprefix("to ")
                elif kind == "Noun":
                    definition = definition.removeprefix("a ")
                    definition = definition.removeprefix("an ")

                # If there is already an English word in the set
                if definition in english_to_anglish:
                    # If there is already a POS of that definition
                    if kind in english_to_anglish[definition]:
                        english_to_anglish[definition][kind].append({
                            "definitions": definitions[1],
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
                                "definitions": definitions[1],
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
                                "definitions": definitions[1],
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