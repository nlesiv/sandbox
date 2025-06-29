import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn import metrics
from sklearn.pipeline import Pipeline

df = pd.read_csv('./TextFiles/moviereviews.tsv', sep='\t')
print(df.head())
print(df.isnull().sum())

# print(df['review'][0])

#clean out null values
df.dropna(inplace=True)
print(df.isnull().sum())

blanks = []
#(index, label, review text)
# Check for blank reviews
for i, lb, rv in df.itertuples():
    if type(rv) == str:
        if rv.isspace():
            blanks.append(i)

df.drop(blanks, inplace=True);
print(len(df))

X = df['review']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


text_clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LinearSVC())
])

model = text_clf.fit(X_train, y_train)
print(model)

predictions = model.predict(X_test)
print(predictions)
print(metrics.classification_report(y_test, predictions))
print(metrics.confusion_matrix(y_test, predictions))
print(metrics.accuracy_score(y_test, predictions))
