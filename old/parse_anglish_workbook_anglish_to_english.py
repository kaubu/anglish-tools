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

anglish_to_english = {}

# Makes "Anglish to English"
with open("in/the_anglish_wordbook.csv", "r") as f:
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

#         print(f"""word = {word}
# anglish_spelling = {anglish_spelling}
# meaning = {meaning}
# kind = {kind}
# forebear = {forebear}
# taken_from = {taken_from}
# notes = {notes}

# all_definitions = {all_definitions}

# ---
# """)

        # Definitions:
        # (['per'], 'per')
        for kind, definitions in all_definitions.items():
            
            kind = kind.replace("PHRASE", "Phrase")
            kind = kind.replace("PREFIX", "Prefix")
            kind = kind.replace("SUFFIX", "Suffix")
            kind = kind.replace("N(PRO)", "Pronoun")
            kind = kind.replace("AJ(P)", "Proper Adjective")
            kind = kind.replace("N(PN)", "Pronoun")
            kind = kind.replace("N(P)", "Proper Noun")
            kind = kind.replace("ADJ", "Adjective")
            kind = kind.replace("ADV", "Adverb")
            kind = kind.replace("AD", "Adverb")
            kind = kind.replace("AJ", "Adjective")
            kind = kind.replace("AV", "Adverb")
            kind = kind.replace("PP", "Prepositional Phrase")
            kind = kind.replace("PN", "Proper Noun")
            kind = kind.replace("AC", "Acronym")
            kind = kind.replace("C", "Conjunction")
            kind = kind.replace("D", "Determiner")
            kind = kind.replace("I", "Interjection")
            kind = kind.replace("N", "Noun")
            kind = kind.replace("P", "Preposition")
            kind = kind.replace("V", "Verb")

            # Fix errors
            kind = kind.replace("Prepositionhrase", "Phrase")
            kind = kind.replace("Prepositionrefix", "Prefix")
            kind = kind.replace("Prepositionronoun", "Pronoun")
            kind = kind.replace("PrepositionroPrepositioner Adjective", "Proper Adjective")
            kind = kind.replace("Noun(PrepositionNoun)", "Pronoun")
            kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            
            for definition in definitions[0]:
                # print(f"definition: {definition}")

                # "to help" → "help"
                # "a soldier" → "soldier"
                # if kind == "Verb":
                #     definition = definition.removeprefix("to ")
                # elif kind == "Noun":
                #     definition = definition.removeprefix("a ")
                #     definition = definition.removeprefix("an ")

                # If there is already an English word in the set
                if word in anglish_to_english:
                    # If there is already a POS of that definition
                    if kind in anglish_to_english[word]:
                        # anglish_to_english[word][kind].append({
                        #     "anglish_word": word,
                        #     "anglish_spelling": anglish_spelling,
                        #     # "pos": kind,
                        #     "definition": definition,
                        #     "forebear": forebear,
                        #     "taken_from": taken_from,
                        #     "notes": notes,
                        # })

                        # English spelling
                        anglish_to_english[word][kind].append(
                            {
                                # "META": {
                                #     "english_spelling": word,
                                #     "anglish_spelling": anglish_spelling,
                                #     "forebear": forebear,
                                #     "taken_from": taken_from,
                                #     "notes": notes,
                                # },
                                # kind: [
                                # {
                                    # "anglish_word": word,
                                "definition": definition,
                                # }
                                # ]
                            }
                        )

                        # Anglish spelling
                        if anglish_spelling != "":
                            anglish_to_english[anglish_spelling][kind].append(
                                {
                                    # "META": {
                                    #     "english_spelling": word,
                                    #     "anglish_spelling": anglish_spelling,
                                    #     "forebear": forebear,
                                    #     "taken_from": taken_from,
                                    #     "notes": notes,
                                    # },
                                    # kind: [
                                    # {
                                        # "anglish_word": word,
                                    "definition": definition,
                                    # }
                                    # ]
                                }
                            )

                    # If the word exists but doesn't have the same kind/POS
                    else:
                        # English spelling
                        anglish_to_english[word].update(
                            {
                                # "META": {
                                #     "english_spelling": word,
                                #     "anglish_spelling": anglish_spelling,
                                #     "forebear": forebear,
                                #     "taken_from": taken_from,
                                #     "notes": notes,
                                # },
                                kind: [
                                    {
                                        # "anglish_word": word,
                                        "definition": definition,
                                    }
                                ]
                            }
                        )

                        # Anglish spelling
                        # Most words don't have an Anglish spelling
                        if anglish_spelling != "":
                            anglish_to_english[anglish_spelling].update(
                                {
                                    "META": {
                                        "english_spelling": word,
                                        "anglish_spelling": anglish_spelling,
                                        "forebear": forebear,
                                        "taken_from": taken_from,
                                        "notes": notes,
                                    },
                                    kind: [
                                        {
                                            # "anglish_word": word,
                                            "definition": definition,
                                        }
                                    ]
                                }
                            )

                # If the word doesn't exist already
                else:
                    # anglish_to_english.update({word: {
                    #     kind: [
                    #         {
                    #             "anglish_word": word,
                    #             "anglish_spelling": anglish_spelling,
                    #             # "pos": kind,
                    #             "definition": definition,
                    #             "forebear": forebear,
                    #             "taken_from": taken_from,
                    #             "notes": notes,
                    #         }
                    #     ]
                    # }})

                    anglish_to_english.update(
                        {
                            word: {
                                "META": {
                                    "english_spelling": word,
                                    "anglish_spelling": anglish_spelling,
                                    "forebear": forebear,
                                    "taken_from": taken_from,
                                    "notes": notes,
                                },
                                kind: [
                                    {
                                        # "anglish_word": word,
                                        "definition": definition,
                                    }
                                ]
                            }
                        }
                    )

                    if anglish_spelling != "":
                        anglish_to_english.update(
                            {
                                anglish_spelling: {
                                    "META": {
                                        "english_spelling": word,
                                        "anglish_spelling": anglish_spelling,
                                        "forebear": forebear,
                                        "taken_from": taken_from,
                                        "notes": notes,
                                    },
                                    kind: [
                                        {
                                            # "anglish_word": word,
                                            "definition": definition,
                                        }
                                    ]
                                }
                            }
                        )
    
        line_count += 1

# print(f"{anglish_to_english}")

with open("out/anglish_to_english.json", "w") as f:
    json.dump(anglish_to_english, f)
