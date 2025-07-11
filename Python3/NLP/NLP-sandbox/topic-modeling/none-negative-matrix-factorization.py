import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer;
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import random
import numpy as np


def getTopNWords(topic, n=10):
    return topic.argsort()[-n:]

def printWordsFromTopic(words, topic,  vectorizer):
    for index in words:
        print(vectorizer.get_feature_names_out()[index], words[index])


npr = pd.read_csv('../TextFiles/npr.csv')
# print(npr.head())


tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')

# cv = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
# dtm = cv.fit_transform(npr['Article'].head())
dtm = tfidf.fit_transform(npr['Article'])
# print(dtm)
nmf_model = NMF(n_components=7, random_state=42)
result = nmf_model.fit(dtm)

print(result)

# Grab the vocbulary of words
features = tfidf.get_feature_names_out()
print(features)

random_word_int = random.randint(0, len(features) -1)
random_feature_names = tfidf.get_feature_names_out()[random_word_int]

print("Random word:", random_feature_names)


# Grab the topics
print(nmf_model.components_)

single_topic = nmf_model.components_[0]
print("Single topic:", single_topic)
# argsort will sort the values and return the list of indices that would sort the array
#get the LAST 10 values in the sorted array
# This will give us the highest probability words for the topic
top_ten_words = single_topic.argsort()[-10:]
top_twenty_words = single_topic.argsort()[-20:]

print("top_twenty_words:", top_twenty_words)
print("top_ten_words:", top_ten_words)

# for index in top_ten_words:
#     print(cv.get_feature_names_out()[index], single_topic[index])

# arr = np.array([10,200,1]).argsort()

# Grab the highest probability words per topic
for index, topic in enumerate(nmf_model.components_):
    print(f"TOpic {index}:")
    print([tfidf.get_feature_names_out()[i] for i in topic.argsort()[-15:]])
    print('\n')


# Transform the document-term matrix to get the topic distribution for each document
# This will give us the topic distribution for each document in the corpus
# Each row corresponds to a document, and each column corresponds to a topic
# The values are the probabilities of each topic for that document
# This is the output of the LDA model
topic_results = nmf_model.transform(dtm)

print(topic_results)

npr['Topic'] = topic_results.argmax(axis=1)
print(npr.head())