# Anglish Tools
Tools to help with Anglish writing.

## Notes

The Anglish Wordbook "meanings" often have "a" or "an" or "the" in front of
nouns, automatically remove it.

For each English word, return to its dictionary form (lemma) and generate all
possible conjugations and declensions, then return the mixed results in the
sidebar.

Some Anglish spelling results don't have the full respelling, just the words
that need respelling. This needs special care. As an example, the respelling of
"the British Sea" is "Britisc".

## Goals

The editor will show an orange underline if there's a Germanic alternative, and
a red underline if there's an Anglish alternative. Anglish is prioritized.

* Germanic
    - [ ] Tell the user when there is a Germanic alternative to a word
    - [ ] Warn the user if the word is not found in the Germanic Thesaurus (can
      be turned off editor-wide or for one word. that word can be saved as a
      part of an ignore list)
* Anglish
    - [ ] Tell the user when there is an Anglish alternative to a word
    - [ ] Show the different senses (adjectives, verbs, nouns, different
      definitions, etc)
    - [ ] Show the alternative (proper) spelling of Anglish words
        * Have a second dictionary consisting of Anglish words with 
    - [ ] 
* Both
    * Editor
        - [ ] Option to hide Anglish spellings
        - [ ] Option to hide Germanic alternatives
        - [ ] Option to hide Anglish alternatives
        - [ ] Option to show additional information about word alternatives,
          such as their forebear, whence it is taken from, and the notes
        - [ ] Ability to dismiss a suggestion or suggestions (for a word)
          temporarily or permanently
            - [ ] Ability to revert dismissals
    * Word search
        - [ ] There is, of course, the standard "exact" results of searches,
          but in case it turns up none or little, there should be a "fuzzy"
          search or "more searches" section where it just searches the entire
          lot and gets anything closely related
        - [ ] Have the website detect when a word is an adjective, noun, verb,
          or all or some. If it's definitely one (plural nouns and conjugated
          verbs will be the easiest to detect) POS, then that will be at the
          top of the suggestions list
