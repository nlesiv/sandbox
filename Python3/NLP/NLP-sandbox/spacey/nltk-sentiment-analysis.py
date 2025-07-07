import nltk
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

a = "this is a good movie"

scores = sid.polarity_scores(a);
print(scores)

b = "This was the best, moast awesome movie EVER MADE!!!!"

scoresB = sid.polarity_scores(b);
print(scoresB);

c = "This was the WORST movie that has ever been created."
scoresC = sid.polarity_scores(c);
print(scoresC)

df = pd.read_csv('../TextFiles/amazonreviews.tsv', sep='\t')
print(df.head())

print(df['label'].value_counts())

blanks = []
df.dropna(inplace=True)
for i, lb, rv in df.itertuples():
    if type(rv) == str:
        if rv.isspace:
            blanks.append(i)

result = sid.polarity_scores(df.iloc[0]['review'])
print(result)

df['scores'] = df['review'].apply(lambda review: sid.polarity_scores(review))
df['compound'] = df['scores'].apply(lambda d:d['compound'])
df['comp_score'] = df['compound'].apply(lambda score: 'pos' if score >= 0 else 'neg')
print(df.head())

print(accuracy_score(df['label'], df['comp_score']))
print(classification_report(df['label'], df['comp_score']))
print(confusion_matrix(df['label'], df['comp_score']))