# ᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫
# Python 3.9 or later

import csv
import json

POS_DIVIDER = "᛬"

def fix_definition(d: str) -> str:
    d = d.replace("[ᛏ]", "(transitive)")
    d = d.replace("ᛏ", "(transitive)")
    d = d.replace("[ᚾ]", "(intransitive: neuter verb)")
    d = d.replace("ᚾ", "(intransitive: neuter verb)")
    d = d.replace("[ᚹ]", "(widened: an expanded meaning given to a word for the sake of Anglisc)")
    d = d.replace("ᚹ", "(widened: an expanded meaning given to a word for the sake of Anglisc)")
    return d

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

def fix_notes(n: str) -> str:
    n = n.replace("PST", "Past Tense")
    n = n.replace("PTCP", "Past Participle")
    n = n.replace("PL", "Plural")

    n = n.replace("[OXF]", "Past Participle")
    n = n.replace("[OED]", "Oxford English Dictionary")
    n = n.replace("[MW]", "Merriam-Webster (though maybe only the 1913 edition)")
    n = n.replace("[CED]", "Collins English Dictionary")
    n = n.replace("[MED]", "Middle English Compendium")
    n = n.replace("[EDD]", "Innsbruck EDD Online 3.0 (based on Joseph Wright’s English Dialect Dictionary, 1898-1905)")

    return n

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

# Makes "English to Anglish"
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
            kind = kind.replace("Prepositionroper Adjective", "Proper Noun / Adjective")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")
            # kind = kind.replace("Prepositionroper Nounoun", "Proper Noun")

            final_definition = fix_definition(definitions[1])
            taken_from = fix_taken_from(taken_from)
            notes = fix_notes(notes)
            
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
                            "anglish_word": word,
                            "anglish_spelling": anglish_spelling,
                            # "pos": kind,
                            "definitions": final_definition,
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
                                # "pos": kind,
                                "definitions": final_definition,
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
                                # "pos": kind,
                                "definitions": final_definition,
                                "forebear": forebear,
                                "taken_from": taken_from,
                                "notes": notes,
                            }
                        ]
                    }})
    
        line_count += 1

with open("out/english_to_anglish.json", "w") as f:
    # f.write(english_to_anglish)
    json.dump(english_to_anglish, f)

######################################
