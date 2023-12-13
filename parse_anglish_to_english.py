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
    new_pos = new_pos.replace("Prepositionrepositional Phrase", "Prepositional Phrase")
    new_pos = new_pos.replace("Prepositionrefix", "Prefix")
    new_pos = new_pos.replace("Prepositionronoun", "Pronoun")
    new_pos = new_pos.replace("PrepositionroPrepositioner Adjective", "Proper Adjective")
    new_pos = new_pos.replace("Noun(PrepositionNoun)", "Pronoun")
    new_pos = new_pos.replace("Prepositionroper Nounoun", "Proper Noun")
    new_pos = new_pos.replace("Prepositionroper Adjective", "Proper Noun and Adjective")

    return new_pos

def fix_definition(d: str) -> str:
    d = d.replace("[ᛏ]", "(transitive)")
    d = d.replace("ᛏ", "(transitive)")
    d = d.replace("[ᚾ]", "(intransitive: neuter verb)")
    d = d.replace("ᚾ", "(intransitive: neuter verb)")
    d = d.replace("[ᚹ]", "(widened: an expanded meaning given to a word for the sake of Anglisc)")
    d = d.replace("ᚹ", "(widened: an expanded meaning given to a word for the sake of Anglisc)")
    return d

taken_from_test = [
    "ANE",
    "NE",
    "ME",
    "OE",
    "WF",
    "LG",
    "HG",
    "NL",
    "Þ",
    "C",
    "I",
    "N",
    "H",
    "O",
]

def fix_taken_from(tf: str) -> str:
    if tf.strip() == "N": return "Norse"
    elif tf.strip() == "Þ": return "Proto-Germanic"
    elif tf.strip() == "C": return "Celtic"
    elif tf.strip() == "I": return "Italic"
    elif tf.strip() == "H": return "Hellenic"
    elif tf.strip() == "O": return "Other"

    tf = tf.replace("ANE", "Archaic New English")
    tf = tf.replace("NE", "New English")
    tf = tf.replace("ME", "Middle English")
    tf = tf.replace("OE", "Old English")
    tf = tf.replace("WF", "West Frisian")
    tf = tf.replace("LG", "Low German")
    tf = tf.replace("HG", "High German")
    tf = tf.replace("NL", "Dutch")
    tf = tf.replace("Þ", "Proto-Germanic")
    tf = tf.replace("C", "Celtic")
    tf = tf.replace("I", "Italic")
    tf = tf.replace("N", "Norse")
    tf = tf.replace("H", "Hellenic")
    tf = tf.replace("O", "Other")

    tf = tf.replace("Archaic Norseew English", "Archaic New English")
    tf = tf.replace("Norseew English", "New English")
    tf = tf.replace("Otherld English", "Old English")
    tf = tf.replace("Hellenicigh German", "High German")
    tf = tf.replace("Norseorse", "Norse")
    # ‹ = immediately from
    # ‹‹ = ultimately from
    tf = tf.replace("‹‹", ", ultimately from ")
    tf = tf.replace("‹", ", from ")
    tf = tf.replace("&", " and ")
    tf = tf.replace("+", " plus ")

    return tf

# for test in taken_from_test:
#     print(f"{test} - {fix_taken_from(test)}")

# input("Close now")

def fix_notes(n: str) -> str:
    n = n.replace("PST", "Past Tense")
    n = n.replace("PTCP", "Past Participle")
    n = n.replace("PL", "Plural")

    n = n.replace("[OXF]", "Past Participle")
    n = n.replace("[OED]", "Oxford English Dictionary")
    n = n.replace("[MW]", "Merriam-Webster (though maybe only the 1913 edition)")
    n = n.replace("[CED]", "Collins English Dictionary")
    n = n.replace("[MED]", "Middle English Compendium")
    n = n.replace("[LEX]", "Lexico (defunct)")
    n = n.replace("[EDD]", "Innsbruck EDD Online 3.0 (based on Joseph Wright’s English Dialect Dictionary, 1898-1905)")

    return n

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
            final_definition = fix_definition(definitions[1])
            taken_from = fix_taken_from(taken_from)
            notes = fix_notes(notes)

            # If the word already has entries, then:
            if anglish_word in anglish_to_english:
                # If there is already a definition with a POS there
                if pos in anglish_to_english[anglish_word]:
                    anglish_to_english[anglish_word][pos].append({
                        "word": anglish_word,
                        "anglish_spelling": anglish_spelling,
                        "definitions": final_definition,
                        "pos": pos,
                        "forebear": forebear,
                        "taken_from": taken_from,
                        "notes": notes,
                        "is_anglish": False,
                    })

                    if anglish_spelling.strip() != "":
                        if anglish_spelling in anglish_to_english:
                            anglish_to_english[anglish_spelling][pos].append({
                                "word": anglish_word,
                                "anglish_spelling": anglish_spelling,
                                "definitions": final_definition,
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                                "is_anglish": True,
                            })
                        else:
                            anglish_to_english.update({
                                anglish_spelling: {
                                    pos: [
                                        {
                                            "word": anglish_word,
                                            "anglish_spelling": anglish_spelling,
                                            "definitions": final_definition,
                                            "pos": pos,
                                            "forebear": forebear,
                                            "taken_from": taken_from,
                                            "notes": notes,
                                            "is_anglish": True,
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
                                "definitions": final_definition,
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                                "is_anglish": False,
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
                                        "definitions": final_definition,
                                        "pos": pos,
                                        "forebear": forebear,
                                        "taken_from": taken_from,
                                        "notes": notes,
                                        "is_anglish": True,
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
                                            "definitions": final_definition,
                                            "pos": pos,
                                            "forebear": forebear,
                                            "taken_from": taken_from,
                                            "notes": notes,
                                            "is_anglish": True,
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
                                "definitions": final_definition,
                                "pos": pos,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                                "is_anglish": False,
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
                                    "definitions": final_definition,
                                    "pos": pos,
                                    "forebear": forebear,
                                    "taken_from": taken_from,
                                    "notes": notes,
                                    "is_anglish": True,
                                }
                            ]
                        }
                    })

with open("out/anglish_to_english.json", "w") as f:
    json.dump(anglish_to_english, f)
