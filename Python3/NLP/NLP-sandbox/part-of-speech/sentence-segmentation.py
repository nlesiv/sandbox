import spacy
from spacy import displacy
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

doc = nlp(u'This is the first sentence. This is another sentence. This is the last sentence.')
for sent in doc.sents:
    print(sent)