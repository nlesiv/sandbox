import spacy
nlp = spacy.load('en_core_web_sm')

print(nlp.Defaults.stop_words)
print(nlp.vocab['mystery'].is_stop)
doc1 = nlp(u"A am a runner running a race in a race because I like to run since I ran the marahon")

for token in doc1:
    print(token.text, '\t', token.lemma_, '\t', token.pos_, '\t', token.dep_, '\t', token.head.text)

