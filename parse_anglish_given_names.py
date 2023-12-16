# English,Anglish,Kind,Whence,Forebear,Foreword,Afterword,Background

import csv
import json

MALE = "♂"
FEMALE = "♀"
UNISEX = "⚥"
DEBUG = False

def process_standard(f, dict_to_save: dict):
    csv_reader = csv.reader(f, delimiter=",")
    line_count = 0

    for row in csv_reader:
        # Ignore the head rows
        if line_count == 0:
            line_count += 1
            continue

        english_name = row[0]   # English spelling of name
        anglish_name = row[1]   # Anglish spelling of name
        kind = row[2]           # Male/Female/Unisex
        whence = row[3]         # Living/Frozen/etc
        forebear = row[4]       # Where the name comes from
        foreword = row[5]       # Where the first half of the word comes
        afterword = row[6]      # Same as above, but the second half
        background = row[7]     # Background information

        if DEBUG:
            print(f"""\nName: {english_name}
Anglish spelling: {anglish_name}
Kind: {kind}
Whence: {whence}
Foreword: {foreword}
Afterword: {afterword}
Background: {background}""")
            input("Continue?")
        
        match kind:
            case "♂":
                kind = "Male"
            case "♀":
                kind = "Female"
            case "⚥":
                kind = "Unisex"
            case n:
                print(f"UNKNOWN KIND: '{n}' at {english_name}")

        if whence in dict_to_save:
            dict_to_save[whence].append({
                "english_name": english_name,
                "anglish_name": anglish_name,
                "kind": kind,
                "whence": whence,
                "forebear": forebear,
                "foreword": foreword,
                "afterword": afterword,
                "background": background,
            })
        else:
            dict_to_save[whence] = [
                {
                    "english_name": english_name,
                    "anglish_name": anglish_name,
                    "kind": kind,
                    "whence": whence,
                    "forebear": forebear,
                    "foreword": foreword,
                    "afterword": afterword,
                    "background": background,
                }
            ]

        line_count += 1

### ANGLISH GIVEN NAMES

anglish_given_names = {}

with open("in/names/anglish_given_names_3.csv", "r") as f:
    process_standard(f, anglish_given_names)

with open("out/anglish_given_names.json", "w") as f:
    # json.dump(anglish_given_names, f, default=set_default)
    json.dump(anglish_given_names, f)

### NORSE GIVEN NAMES

anglo_norse_given_names = {}

with open("in/names/anglo-norse_given_names.csv", "r") as f:
    process_standard(f, anglo_norse_given_names)

with open("out/anglo-norse_given_names.json", "w") as f:
    json.dump(anglo_norse_given_names, f)
