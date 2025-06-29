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

df = pd.read_csv('./TextFiles/smsspamcollection.tsv', sep='\t')
print(df.head())
print(df.isnull().sum())

print(df['label'].value_counts())

X = df['message']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#----- These steps are for show only they can be combined into one step with TfidfVectorizer -----

# count_vect = CountVectorizer();
# # Fit the vectorizer to the data (Build a vocab, count the number of words...)
# count_vect.fit(X_train)

# # Transform the original text data into mesasge --> Vector
# X_train_counts = count_vect.transform(X_train)

# # print(X_train_counts)
# print(X_train.shape)
# print(X_train_counts.shape)

# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# print(X_train_tfidf.shape)

#----- End EXample of expanded count vectorization and tf-idf transformation -----

#--- Example of using TfidfVectorizer directly ---
# Create a TF-IDF Vectorizer (This combines the CountVectorizer and TfidfTransformer)
# tfidf_vectorizer = TfidfVectorizer()
# # Fit the vectorizer to the training data and transform it
# X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

# print(X_train_tfidf.shape)

# clf = LinearSVC()
# result = clf.fit(X_train_tfidf, y_train)
# print(result)

#-- End Example of using TfidfVectorizer directly ---

# --- Example of using a Pipeline with TfidfVectorizer and LinearSVC ---
# This combines the vectorization and classification into a single step
# This is the preferred way to do it in scikit-learn
# It allows for easier cross-validation and hyperparameter tuning
# It also makes the code cleaner and more maintainable
# The pipeline will first vectorize the text data and then fit the classifier
# This is the most common way to use scikit-learn for text classification tasks
# It is also the most efficient way to do it, as it avoids the need to store
# intermediate results in memory, which can be a problem for large datasets

text_clf = Pipeline([('tfidf', TfidfVectorizer()),('clf', LinearSVC())])

result = text_clf.fit(X_train, y_train)
print(result)
predictions = text_clf.predict(X_test)

print(metrics.confusion_matrix(y_test, predictions))
print(metrics.classification_report(y_test, predictions))
print(metrics.accuracy_score(y_test, predictions))

