# English,Anglish,Kind,Whence,Forebear,Foreword,Afterword,Background

import csv
import json

MALE = "♂"
FEMALE = "♀"
UNISEX = "⚥"
DEBUG = False

anglish_given_names = {}

with open("in/anglish_given_names.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")

    for row in csv_reader:
        english_name = row[0]   # English spelling of name
        anglish_name = row[1]   # Anglish spelling of name
        kind = row[2]           # Male/Female/Unisex
        whence = row[3]         # Living/Frozen/etc
        foreword = row[4]       # Where the first half of the word comes
        afterword = row[5]      # Same as above, but the second half
        background = row[6]     # Background information

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

        if whence in anglish_given_names:
            anglish_given_names[whence].append({
                "english_name": english_name,
                "anglish_name": anglish_name,
                "kind": kind,
                "whence": whence,
                "foreword": foreword,
                "afterword": afterword,
                "background": background,
            })
        else:
            anglish_given_names[whence] = [
                {
                    "english_name": english_name,
                    "anglish_name": anglish_name,
                    "kind": kind,
                    "whence": whence,
                    "foreword": foreword,
                    "afterword": afterword,
                    "background": background,
                }
            ]

# def set_default(obj):
#     if isinstance(obj, set):
#         return list(obj)
#     raise TypeError

with open("out/anglish_given_names.json", "w") as f:
    # json.dump(anglish_given_names, f, default=set_default)
    json.dump(anglish_given_names, f)
