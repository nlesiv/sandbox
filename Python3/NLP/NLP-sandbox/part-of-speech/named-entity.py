import spacy
from spacy import displacy
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

def show_named_entities(doc):
    if doc.ents:
        for ent in doc.ents:
            print(f"{ent.text} ({ent.label_}) - {spacy.explain(ent.label_)}")
    else:
        print("No named entities found.")

doc = nlp(u"Hi how are you?")
show_named_entities(doc)

doc2 = nlp(u"May I got to Washington DC?")
show_named_entities(doc2)

doc3 = nlp(u"Tesla to build a new U.K. factory for $6 million.")
show_named_entities(doc3)

ORG = doc.vocab.strings[u"ORG"]
new_ent = Span(doc3, 0, 1, label=ORG)
doc3.ents = list(doc3.ents) + [new_ent]

show_named_entities(doc3)


doc4 = nlp(u"Our company created a brand new vacuum cleaner."
           u"This new vacuum-cleaner is the best in show.")

matcher = PhraseMatcher(nlp.vocab)
phrase_list = ['vacuum cleaner', 'vacuum-cleaner']
patterns = [nlp(text) for text in phrase_list]
matcher.add('newproduct', None, *patterns)

found_matches = matcher(doc4)
print(found_matches)

PROD = doc.vocab.strings[u"PRODUCT"]
new_ent4 = [Span(doc4, match[1], match[2],label=PROD) for match in found_matches]

doc4.ents = list(doc4.ents) + new_ent4

show_named_entities(doc4)

doc5 = nlp(u"Originally I paid $29.95 for this car toy, but now it is marked down by 10 dollars.")

[ent for ent in doc5.ents if ent.label_ == 'MONEY']
print(len(doc5.ents))

displacy.serve(doc4, style='ent')