import spacy;

# Load the English NLP model
# Make sure to have the model installed with: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

doc = nlp(u'Tesla is looking at buying U.S. startup for $6 billion')
for token in doc:
    # POS: Part of Speech
    # dep: Dependency relation
    # head: Syntactic head of the token
    # text: The original text of the token
    print(token.text, token.pos_, token.dep_, token.head.text)

print(nlp.pipeline)
print(nlp.pipe_names)

doc2 = nlp(u"Tesla isnt' looking to buy a startup anymore.")
for token in doc2:
    # POS: Part of Speech
    # dep: Dependency relation
    # head: Syntactic head of the token
    # text: The original text of the token
    print(token.text, token.pos_, token.dep_, token.head.text)

print(doc2[0].pos_)

doc3 = nlp(u'Although commmonly attributed to John Lennon from his song "Beautiful Boy", \
the phrase "Life is what happens to us while we are making other plans" was written by \
cartoonist Allen Saunders and published in Reader\'s Digest in 1957, when Lennon was 17.')

life_quote = doc3[16:30]

print(life_quote)