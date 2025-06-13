import spacy;

# Load the English NLP model
# Make sure to have the model installed with: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

mystring = '"We\'re moving to L.A.!"'

doc = nlp(mystring)

for token in doc:
    print(token.text, end=' | ')


doc2 = nlp(u"We're here to help! Send snail-mail, email support@oursite.com or visit us at http://www.oursite.com!")

for t in doc2:
    print(t)

doc3 = nlp(u'A 5km NYC cab ride costs $10.30')

for t in doc3:
    print(t)

doc4 = nlp(u"Let's visit St. Louis in the U.S. next year.")

for t in doc4:
    print(t)


len(doc)
len(doc.vocab)

doc5 = nlp(u'It is better to give than to receive.')

# Retrieve the third token:
doc5[2]


doc9 = nlp(u"Autonomous cars shift insurance liability toward manufacturers.")

for chunk in doc9.noun_chunks:
    print(chunk.text)

doc10 = nlp(u"Red cars do not carry higher insurance rates.")

for chunk in doc10.noun_chunks:
    print(chunk.text)

doc11 = nlp(u"He was a one-eyed, one-horned, flying, purple people-eater.")

for chunk in doc11.noun_chunks:
    print(chunk.text)