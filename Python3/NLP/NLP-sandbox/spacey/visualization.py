import spacy;
from spacy import displacy;

# Load the English NLP model
# Make sure to have the model installed with: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

doc = nlp(u'Apple is going to build a U.K. factory for $6 million.')

# displacy.render(doc, style='dep', jupyter=False, options={'distance': 90})
displacy.serve(doc, style='dep', port=8090)

doc2 = nlp(u"Over the last quarter, apple sold nearly 20 million iPhone for a total profit of $12 billion.")
# displacy.render(doc2, style='ent', jupyter=False, options={'distance': 90})
