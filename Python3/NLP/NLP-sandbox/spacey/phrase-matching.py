import spacy;
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


# Load the English NLP model
# Make sure to have the model installed with: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

matcher = Matcher(nlp.vocab)

# SolarPower
pattern1 = [{'LOWER': 'solarpower'}]
# solar-power
pattern2 = [{'LOWER': 'solar'}, {"IS_PUNCT": True, 'OP': '*'}, {"LOWER": "power"}]
# Solar power
pattern3 = [{'LOWER': 'solar'}, {'LOWER': 'power'}]

matcher.add("SolarPower", patterns=[pattern1, pattern2, pattern3])
doc = nlp(u"SolarPower is a great company. Solar--power is also good. Solar power is the future.")

matches = matcher(doc)
print(matches)

# phrase matches
matcher = PhraseMatcher(nlp.vocab)
phrase_list = ['voodoo economics', 'supply-side economics', 'trickle-down economics', 'free-market economics']
phrase_patterns = [nlp(text) for text in phrase_list]
with open("./TextFiles/reaganomics.txt",'r', encoding="cp1252") as f:
    doc3 = nlp(f.read())
matcher.add("EconMatcher", None, *phrase_patterns)
found_matches = matcher(doc3)
print(found_matches)