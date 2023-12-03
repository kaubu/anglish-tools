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

def fix_pos(pos: str) -> str:
    new_pos = pos.replace("PHRASE", "Phrase")
    new_pos = new_pos.replace("SUFFIX", "Suffix")
    new_pos = new_pos.replace("PREFIX", "Prefix")
    new_pos = new_pos.replace("N(PRO)", "Pronoun")
    new_pos = new_pos.replace("AJ(P)", "Proper Adjective")
    new_pos = new_pos.replace("N(PN)", "Pronoun")
    new_pos = new_pos.replace("N(P)", "Proper Noun")
    new_pos = new_pos.replace("ADJ", "Adjective")
    new_pos = new_pos.replace("ADV", "Adverb")
    new_pos = new_pos.replace("AD", "Adverb")
    new_pos = new_pos.replace("AJ", "Adjective")
    new_pos = new_pos.replace("AV", "Adverb")
    new_pos = new_pos.replace("PP", "Prepositional Phrase")
    new_pos = new_pos.replace("PN", "Proper Noun")
    new_pos = new_pos.replace("AC", "Acronym")
    new_pos = new_pos.replace("C", "Conjunction")
    new_pos = new_pos.replace("D", "Determiner")
    new_pos = new_pos.replace("I", "Interjection")
    new_pos = new_pos.replace("N", "Noun")
    new_pos = new_pos.replace("P", "Preposition")
    new_pos = new_pos.replace("V", "Verb")

    # Fix errors
    new_pos = new_pos.replace("Prepositionhrase", "Phrase")
    new_pos = new_pos.replace("Prepositionrefix", "Prefix")
    new_pos = new_pos.replace("Prepositionronoun", "Pronoun")
    new_pos = new_pos.replace("PrepositionroPrepositioner Adjective", "Proper Adjective")
    new_pos = new_pos.replace("Noun(PrepositionNoun)", "Pronoun")
    new_pos = new_pos.replace("Prepositionroper Nounoun", "Proper Noun")
    new_pos = new_pos.replace("Prepositionroper Adjective", "Proper Noun and Adjective")

    return new_pos

anglish_to_english = {}

# Makes "Anglish to English"
with open("in/the_anglish_wordbook.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")
    line_count = 0
    
    for row in csv_reader:
        # row = word.split(",", 7);

        anglish_word = row[0]
        anglish_spelling = row[1]
        raw_definitions = row[2]   # No use after definitions
        pos = row[3]      # No use after definitions
        forebear = row[4]
        taken_from = row[5]
        notes = row[6]

        # POS and definitions grouped
        formatted_definitions = split_definitions(raw_definitions, pos)

        for pos, definitions in formatted_definitions.items():
            # definitions[0] = definitions split into a list
            # ['enduring', 'continuing']
            # definitions[1] = definitions still in one string
            # 'enduring, continuing'

            pos = fix_pos(pos)

            # If the word already has entries, then:
            if anglish_word in anglish_to_english:
                # If there is already a definition with a POS there
                if pos in anglish_to_english[anglish_word]:
                    anglish_to_english[anglish_word][pos].append({
                        "word": anglish_word,
                        "anglish_spelling": anglish_spelling,
                        "definitions": definitions[1],
                        "pos": pos,
                        "forebear": forebear,
                        "taken_from": taken_from,
                        "notes": notes,
                    })

                    if anglish_spelling.strip() != "":
                        if anglish_spelling in anglish_to_english:
                            anglish_to_english[anglish_spelling][pos].append({
                                "word": anglish_word,
                                "anglish_spelling": anglish_spelling,
                                "definitions": definitions[1],
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            })
                        else:
                            anglish_to_english.update({
                                anglish_spelling: {
                                    pos: [
                                        {
                                            "word": anglish_word,
                                            "anglish_spelling": anglish_spelling,
                                            "definitions": definitions[1],
                                            "pos": pos,
                                            "forebear": forebear,
                                            "taken_from": taken_from,
                                            "notes": notes,
                                        }
                                    ]
                                }
                            })
                # If there is no POS in that word's entry
                else:
                    anglish_to_english[anglish_word].update({
                        pos: [
                            {
                                "word": anglish_word,
                                "anglish_spelling": anglish_spelling,
                                "definitions": definitions[1],
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            }
                        ]
                    })

                    if anglish_spelling.strip() != "":
                        if anglish_spelling in anglish_to_english:
                            anglish_to_english[anglish_spelling].update({
                                pos: [
                                    {
                                        "word": anglish_word,
                                        "anglish_spelling": anglish_spelling,
                                        "definitions": definitions[1],
                                        "pos": pos,
                                        "forebear": forebear,
                                        "taken_from": taken_from,
                                        "notes": notes,
                                    }
                                ]
                            })
                        else:
                            anglish_to_english.update({
                                anglish_spelling: {
                                    pos: [
                                        {
                                            "word": anglish_word,
                                            "anglish_spelling": anglish_spelling,
                                            "definitions": definitions[1],
                                            "pos": pos,
                                            "forebear": forebear,
                                            "taken_from": taken_from,
                                            "notes": notes,
                                        }
                                    ]
                                }
                            })

            # If the word has no entries:
            else:
                anglish_to_english.update({
                    anglish_word: {
                        pos: [
                            {
                                "word": anglish_word,
                                "anglish_spelling": anglish_spelling,
                                "definitions": definitions[1],
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            }
                        ]
                    }
                })

                if anglish_spelling.strip != "":
                    anglish_to_english.update({
                        anglish_spelling: {
                            pos: [
                                {
                                    "word": anglish_word,
                                    "anglish_spelling": anglish_spelling,
                                    "definitions": definitions[1],
                                    "pos": pos,
                                    "forebear": forebear,
                                    "taken_from": taken_from,
                                    "notes": notes,
                                }
                            ]
                        }
                    })

with open("out/anglish_to_english.json", "w") as f:
    json.dump(anglish_to_english, f)
