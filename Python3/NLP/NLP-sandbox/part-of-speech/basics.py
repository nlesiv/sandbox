import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(u"The quick brown fox jumped over the lazy dog's back.")
print(doc.text)

print(doc[4].tag_) # detailed part of speech tag
print(doc[4].pos_) # part of speech

for token in doc:
    print(f"{token.text:<12} {token.tag_:<10} {token.pos_:<10} {token.dep_:<10} {token.head.text:<12} {token.shape_:<6} {token.is_alpha:<5} {token.is_stop:<5}")

POS_count = doc.count_by(spacy.attrs.POS);
for k, v in sorted(POS_count.items()):
    print(f"{k}. {doc.vocab[k].text:{5}} {v}")


TAG_count = doc.count_by(spacy.attrs.TAG);
for k, v in sorted(TAG_count.items()):
    print(f"{k}. {doc.vocab[k].text:{5}} {v}")

options = {'distance': 110, 'compact': True, 'color': 'yellow', 'bg': '#09a3d5', 'font': 'Times'}
displacy.serve(doc, style="dep", options=options)
