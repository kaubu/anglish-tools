# ᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫
# Python 3.9 or later

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

split_definitions_examples = [
    ["᛫ delicate and tendril-like ᛫ diaphanous ᛫ gauzy ᛫ airy ᛫", "AJ"],
    [" 	᛫ a region in Poland ᛫", "N(P)"],
    [" 	᛫ guidance ᛫ instruction ᛫", "N"],
    ["᛫ weak ᛫ watery ᛫ feeble wavering ᛫", "AJ"],
    ["᛫ a manner ᛫ a fashion ᛫ a method ᛬ to make apparent ᛬ sagacious ᛫ prudent ᛫", "N᛬V᛬AJ"]
]

for s in split_definitions_examples:
    a = split_definitions(s[0], s[1])
    print(a)