import spacy
from scipy import spatial

nlp = spacy.load("en_core_web_lg")

# print(nlp(u"the quick brown fox jumped").vector)

# tokens = nlp(u'lion cat pet')
tokens = nlp("like love hate nargle")
for token1 in tokens:
    for token2 in tokens:
        print(
            token1.text,
            token2.text,
            token1.similarity(token2),
            token1.has_vector,
            token1.vector_norm,
            token1.is_oov,
        )

print(len(nlp.vocab.vectors))
print(nlp.vocab.vectors.shape)

# cosine similarity
cosine_similarity = lambda vec1, vec2: 1 - spatial.distance.cosine(vec1, vec2)

king = nlp.vocab["king"].vector
man = nlp.vocab["man"].vector
woman = nlp.vocab["women"].vector

# king - man + woman -> new Vector similar to queen, princess, highness
new_vector = king - man + woman

computed_similarities = []
for word in nlp.vocab:
    if word.has_vector:
        if word.is_lower:
            if word.is_alpha:
                similarity = cosine_similarity(new_vector, word.vector)
                computed_similarities.append((word, similarity))

computed_similarities = sorted(computed_similarities, key=lambda item: -item[1])
for word, similarity in computed_similarities[:10]:
    print(word.text, similarity)
